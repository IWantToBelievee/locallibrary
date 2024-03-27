from django.urls import re_path, path
from catalog import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(
        r'^books/$',
        views.book_list,
        name='books'
    ),
    re_path(
        r'^book/(?P<pk>\d+)$',
        views.BookDetailView.as_view(),
        name='book-detail'
    ),
    re_path(
        r'^authors/$',
        views.AuthorListView.as_view(),
        name='authors'
    ),
    re_path(
        r'^author/(?P<pk>\d+)$',
        views.AuthorDetailView.as_view(),
        name='author-detail'
    ),
    re_path(
        "^profile/(?P<pk>\d+)$",
        views.ProfileView.as_view(),
        name="profile"
    ),
    path('books_json/', views.book_list_json),
    path('books_json/<int:pk>/', views.book_detail_json),
    path('authors_json/', views.author_list_json),
    path('authors_json/<int:pk>/', views.author_detail_json),
]
