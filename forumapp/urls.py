from django.urls import path
from .views import *
from . import views
app_name = "forumapp"

urlpatterns = [

    #home page
    path("",HomeView.as_view(),name = "home"), #home page 

    #home page
    path('latest/question/',LatestQuestionView.as_view(),name = "latestquestion"),


    #register page
    path('register/',RegisterView.as_view(), name='register'), #user register page
    # path('register1',views.signup_view,name='register1'),
    # path("login/",LoginView.as_view(),name = "login"),
    path("login/user/",views.LoginFormView,name = 'login'), #user login page
#     path('question/add/',QuestionAddView.as_view(),name = "questionadd"),
    path('question/add/',views.QuestionAddView,name = "questionadd"),



    path('question/confirm/',views.QuestionConfirmView,name="question-confirm"),

    # path('question/<int:pk>/details/', QuestionDetailView.as_view(), name='questiondetail'),
    path('question/<int:pk>/details/',views.QuestionDetailView,name = "questiondetail"),

    #editview of answer
    path('question/update/<int:pk>/',
         QuestionUpdateView.as_view(), name='question_update'),


    #deleteview of answer
    path('question/delete/<int:pk>/',
         QuestionDeleteView.as_view(), name='question_delete'),


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

     path('search/question/',views.SearchView, name = 'search'),

     ############ logout ##########
     path('logout/',LogoutView.as_view(),name='logout'),

     ### category based display 
     path("category/questions/education/",CategoryEducationView.as_view(),name='categorylist'),

     path("category/questions/sports/",CategorySportsView.as_view(),name='category_sports'),

     path("category/questions/politics/",CategoryPoliticsView.as_view(),name='category_politics'),

     path("category/questions/fashion_and_style/",CategoryFashionView.as_view(),name='category_fashion'),

     path("category/questions/health/",CategoryHealthView.as_view(),name='category_health'),

     path("category/questions/it/",CategoryItView.as_view(),name='category_it'),




     ##view the users by admin
     path('admin/view-questions/',QuestionView.as_view(),name='questionview'),

     path('admin/view-users/',UserView.as_view(),name='userview'),


    

    


]