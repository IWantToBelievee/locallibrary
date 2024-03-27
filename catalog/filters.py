from django_filters import *
from .models import Book


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = ['author', 'genre']
