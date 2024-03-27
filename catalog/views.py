from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre, Language
from catalog.forms import FilterForm, SortListForm
from django.core.paginator import Paginator as P
from .filters import BookFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from catalog.serializers import BookSerializer, AuthorSerializer


# index page
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    return render(request, 'catalog/index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    })


def book_list(request):
    queryset = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=queryset)

    if request.method == 'POST':
        filter_form = FilterForm(request.POST)
        sort_form = SortListForm(request.POST)
        if filter_form.is_valid():
            year = str(filter_form.cleaned_data.get('year'))
            month = str(filter_form.cleaned_data.get('month'))
            day = str(filter_form.cleaned_data.get('day'))
            genre = str(filter_form.cleaned_data.get('genre'))
            author = str(filter_form.cleaned_data.get('author'))

            m = month if len(month) == 2 else f'0{month}' if len(month) != 0 else ""
            d = day if len(day) == 2 else f'0{day}' if len(day) != 0 else ""

            fltr_r_d = ""
            fltr_g = ""
            fltr_a = ["", ""]

            if day and month and year:
                fltr_r_d = f"{year}-{m}-{d}"
            if not day and month and year:
                fltr_r_d = f"{year}-{m}"
            if not day and not month and year:
                fltr_r_d = year

            if genre:
                fltr_g = genre

            if author:
                fltr_a = author.split()

            queryset = queryset.filter(release_date__contains=fltr_r_d,
                                       genre__name__contains=fltr_g,
                                       author__first_name__icontains=fltr_a[0],
                                       author__last_name__icontains=fltr_a[1])

        if sort_form.is_valid():
            order = sort_form.cleaned_data.get("order")

            if order == "1":
                queryset = queryset.order_by("title")
            elif order == "2":
                queryset = queryset.order_by("-title")
    else:
        filter_form = FilterForm()
        sort_form = SortListForm()

    paginate_by = 2
    paginator = P(book_filter.qs, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = len(book_filter.qs) > paginate_by

    context = {'filter_form': filter_form,
               'sort_form': sort_form,
               'obj_last': list(Book.objects.all())[-1],
               'paginator': paginator,
               'page_obj': page_obj,
               'is_paginated': is_paginated,
               'page_count': [i for i in range(1, paginate_by+1)],
               'pag_step': paginate_by,
               'book_list': queryset,
               'book_filter': book_filter,
               }

    return render(request, template_name='catalog/book_list.html', context=context)


class BookDetailView(generic.DetailView):
    model = Book


# AUTHOR list and detail views >>>

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    queryset = Author.objects.all()
    template_name = 'catalog/author_list.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)

        context['author_list_last'] = list(Author.objects.all())[-1]

        return context


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)

        return context


class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'catalog/profile.html'
    model = BookInstance
    paginate_by = 5
    context_object_name = 'borrowed_list'

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user, status__exact='o')
                .order_by('due_back')
        )


@csrf_exempt
def book_list_json(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def book_detail_json(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
       serializer = BookSerializer(book)
       return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


@csrf_exempt
def author_list_json(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def author_detail_json(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
       serializer = AuthorSerializer(author)
       return JsonResponse(serializer.data)
    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = BookSerializer(author, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)
    # elif request.method == 'DELETE':
    #     author.delete()
    #     return HttpResponse(status=204)