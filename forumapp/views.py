
from django.shortcuts import render
from django.views.generic import *
# Create your views here.


class HomeView(TemplateView):
    print('this is good')
    template_name = 'forum/test.html'
