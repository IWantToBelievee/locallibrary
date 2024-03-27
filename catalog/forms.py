from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class FilterForm(forms.Form):
    # release date
    year = forms.CharField(max_length=4, required=False)
    month = forms.CharField(max_length=2, required=False)
    day = forms.CharField(max_length=2, required=False)

    # genre
    genre = forms.CharField(required=False)

    # author
    author = forms.CharField(required=False)


class SortListForm(forms.Form):
    choices = (
        ("1", "Alphabetically - Ascending"),
        ("2", "Alphabetically - Descending"),
    )
    order = forms.ChoiceField(choices=choices)

