from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView as LV

import datetime


class LoginView(LV):
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        current_time = datetime.datetime.now().hour
        if 6 <= current_time < 12:
            context['current'] = 'morning'
        elif 12 < current_time < 18:
            context['current'] = 'day'
        elif 18 <= current_time <= 23:
            context['current'] = 'evening'
        elif 0 <= current_time < 6:
            context['current'] = 'night'

        return context