import datetime
from datetime import date
import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=200,
                            help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


def default_date():
    now = datetime.datetime.now()
    start_time = now.replace(year=0000, month=00, day=00)
    return start_time


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author',
                               on_delete=models.SET_NULL,
                               null=True)

    summary = models.TextField(max_length=1000,
                               help_text="Enter a brief description of the book")

    genre = models.ManyToManyField('Genre',
                                   help_text="Select a genre for this book")

    release_date = models.CharField(max_length=10, help_text="Book release date(yyyy-mm-dd)",
                                    null=True,
                                    blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def summary_offset(self):
        return "    " + self.summary


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")

    book = models.ForeignKey('Book',
                             on_delete=models.SET_NULL,
                             null=True)

    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL,
                                 null=True)

    imprint = models.CharField(max_length=200)

    isbn = models.CharField(max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                            null=True,
                            blank=True)

    due_back = models.DateField(null=True,
                                blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(choices=LOAN_STATUS,
                              max_length=1,
                              blank=True,
                              default='m',
                              help_text="Book availability")

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)


class Author(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True,
                                     blank=True)

    date_of_death = models.DateField('Died',
                                     null=True,
                                     blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Language(models.Model):

    language = models.CharField(max_length=30,
                                help_text="Language of imprint")

    def __str__(self):
        return self.language



