from django.urls import path
from .views import *

app_name = "forumapp"

urlpatterns = [
    path("",HomeView.as_view(),name = "home"),
    path("login/user/",LoginRegisterView.as_view(),name = "loginregister")

]