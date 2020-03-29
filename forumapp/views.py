
from django.shortcuts import render
from django.views.generic import *
# Create your views here.


class HomeView(TemplateView):
    print('this is good')
    template_name = 'forum/test.html'

class LoginRegisterView(TemplateView):
    print('this is login')
    template_name = 'user/userlogin.html'