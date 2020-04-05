from django.urls import path
from .views import *
from . import views
app_name = "forumapp"

urlpatterns = [
    path("home/",HomeView.as_view(),name = "home"),
    path("test/",TestView.as_view(),name = "test"),

    path('register/',RegisterView.as_view(), name='register'),
    # path('register1',views.signup_view,name='register1'),
    # path("login/",LoginView.as_view(),name = "login"),
    path("login/user/",views.LoginFormView,name = 'login')

]