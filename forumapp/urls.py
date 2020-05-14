from django.urls import path
from .views import *
from . import views
app_name = "forumapp"

urlpatterns = [

    #home page
    path("",HomeView.as_view(),name = "home"), #home page 

    #register page
    path('register/',RegisterView.as_view(), name='register'), #user register page
    # path('register1',views.signup_view,name='register1'),
    # path("login/",LoginView.as_view(),name = "login"),
    path("login/user/",views.LoginFormView,name = 'login'), #user login page
    path('question/add/',QuestionAddView.as_view(),name = "questionadd"),

    # path('question/<int:pk>/details/', QuestionDetailView.as_view(), name='questiondetail'),
    path('question/<int:pk>/details/',views.QuestionDetailView,name = "questiondetail"),

    #like button
    # path('user/<int:pk>/like/',views.LikeView,name="liked")
    path('user/like/',views.LikeView,name="liked"),

    path('user/like/answer/',views.LikeAnswerView,name="liked_answer"),

    #editview of answer
    path('answer/update/<int:pk>/',
         AnswerUpdateView.as_view(), name='answerupdate'),


    #deleteview of answer
    path('answer/delete/<int:pk>/',
         AnswerDeleteView.as_view(), name='answerdelete'),


     #### show notifications
     # path("notify/<int:pk>/",views.ShowNotification,name='notification'),

     path('notify/', views.NotificationListView.as_view(), name='notifications'),


     # path("notify/<int:pk>/",views.TestNotification,name='testnotification'),





    

    


]