from django.urls import path
from .views import *
from . import views
app_name = "forumapp"

urlpatterns = [
    path("",HomeView.as_view(),name = "home"), #home page 

    path('register/',RegisterView.as_view(), name='register'), #user register page
    # path('register1',views.signup_view,name='register1'),
    # path("login/",LoginView.as_view(),name = "login"),
    path("login/user/",views.LoginFormView,name = 'login'), #user login page
    path('question/add/',QuestionAddView.as_view(),name = "questionadd"),
    # path('question/create/',views.QuestionCreateView,name='questioncreate'),


]