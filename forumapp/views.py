
from django.shortcuts import render,redirect,reverse,get_object_or_404,render_to_response
from django.views.generic import *
from .forms import UserForm,LoginForm,QuestionForm,AnswerForm,QuestionLikeForm,QuestionUpdateForm,QuestionFilter
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView
from django.db.models import Count
from django.db.models import Q
from django.template.context import RequestContext
from django.contrib.messages.views import SuccessMessageMixin
from forumapp.utils.predict_tag import predict_tag

# Create your views here.
import language_check
from django.http import JsonResponse
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from autocorrect import Speller

"""
Homepage

"""
class HomeView(TemplateView):
    template_name = 'forum/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()[:4]
        context['answers'] = Answer.objects.all()

        # context['users'] = NormalUser.objects.all()
        # print('logged in user',context['users'])
        # context['answer-count'] = Question.objects.annotate(number_of_answers=Count('answer'))

        # context['profile'] = NormalUser.objects.get(id = self.request.user.id)
        context['form'] = AnswerForm()
        
        
        return context

        # {% if question.image %}<div class="user"><img src="{{ question.normal_user.image.url }}"></div>{% endif %} 

"""
LatestQuestionView
"""
class LatestQuestionView(TemplateView):
    template_name = 'forum/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()[:4]
        context['answers'] = Answer.objects.all()
        
        # context['profile'] = NormalUser.objects.get(id = self.request.user.id)
        context['form'] = AnswerForm()
        
        
        return context




####################### login form ###############

"""
login form

"""
class LoginRegisterView(TemplateView):
    template_name = 'user/userlogin.html'
# def RegisterView(request):
#     if request.method == "POST":
#         form_class = UserForm
#         print('this is form class')
#         uname = request.POST.get('username')
#         pword = request.POST.get('password')
#         user = authenticate(request,username = uname,password = pword)
#         print(user)
#         if user is not None:
#             login(request,user)
#             return render('forumapp:home')

#     else:
#         form = UserForm
#     return render(request,'userlogin.html',)



"""
register form

"""
class RegisterView(CreateView):
    template_name = 'user/userlogin.html'
    form_class = UserForm
    success_url = reverse_lazy('forumapp:login')

    def form_valid(self, form):
        u_name = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = User.objects.create_user(u_name, '', pword)
        form.instance.user = user
        # login(self.request, user)
        return super().form_valid(form)




"""
login form
"""
def LoginFormView(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        user = authenticate(username=uname,password=pword)
        if user:
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('forumapp:adminhome'))
                else:
                    return HttpResponseRedirect(reverse('forumapp:home'))
        else:
            return render(request,'user/login.html',{
                'messages': 'Your username doesnot exist',
                'form': LoginForm
            })
            # return HttpResponse("your username did not match")
    
    else:
        form = LoginForm
        return render(request,'user/login.html',{'form':form})
    



"""
Question add

"""
# class QuestionAddView(BSModalCreateView):
#     print('this is add view')
#     template_name = "question/questioncreate.html"
#     form_class = QuestionForm

#     success_url = reverse_lazy('forumapp:home')
#     success_message = "Question has been added"


#     def form_valid(self,form):
#         print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&77')

#         usr = self.request.user
#         print('user = ',usr)
#         question_user = NormalUser.objects.get(user = usr)
#         print('question user',question_user)
#         form.instance.user_q = question_user
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super(QuestionAddView, self).get_context_data(**kwargs)
#         predict_test = prediction()
#         return ctx
# def QuestionAddView(request):
#     print("request = ",request)
#     if request.method == 'POST':
#         print('this is post request')
#         question = request.POST['question_form']
#         print("question = = ",question)
#         if form.is_valid():
#              cd = form.cleaned_data
#              # assert False
#              return HttpResponseRedirect('/contact?submitted=True')
#     else:
#         print("this is else in form")
#         form = QuestionForm() 
#     return render(request,'question/questioncreate.html',{'form': form})
"""
question add
"""
@login_required(login_url='/login/user/')
def QuestionAddView(request):
    if request.method == 'GET':
        print('this is 1st one')
        form = QuestionForm()
        context = {
            'form': form
        }
        return render(request, 'question/questioncreate.html', context)

    else:
        if request.method == "POST":
            # confirm_question = request.POST.get['final_que']
            question = request.POST.get('final_que',None)
            print("this is inputed questions",question)
            predict = predict_tag(question)
            print("precictcc",predict)
            # confirm_question= request.POST.get("final_que")
            log_user = NormalUser.objects.get(user = request.user)
            Question.objects.create(user_q = log_user,question = question,category = predict)            
            context = {
                'ram':'ram'
            }
            return render(request, 'question/questioncreate.html',context)

"""
question confirm
"""
def QuestionConfirmView(request):

    if request.method == 'POST':

        # Receive data from client
        question = request.POST.get('myquestion')
        spell = Speller(lang='en')
        confirm_ques = spell(question)
        print("confirm_ques###########",confirm_ques)
        # tool = language_check.LanguageTool('en-US')
        # texts = question
        # matches = tool.check(texts)
        # confirm_ques = language_check.correct(texts, matches)


        
        context = {
            'confirm_ques':confirm_ques
        }
        # return JsonResponse({'sepal_length': sepal_length,
        # })
        return render(request, 'question/question_confirm.html',context)
        # return render(request,"question/questioncreate.html",{'sepal_length':sepal_length})
    else:
            # confirm_question = request.POST.get['final_que']
        confirm_question= request.GET.get("confirm_ques")
        context = {
                'ram':'ram'
        }
        return render(request, 'question/questioncreate.html',context)





"""
details of question

"""
def QuestionDetailView(request,pk):
    questions = get_object_or_404(Question,pk=pk)
    ##show the similar posts
    similar_questions = Question.objects.filter(category = questions.category)
    page = request.GET.get('page', 1)

    #page display a questions in 10 pages
    paginator = Paginator(similar_questions, 10)

    try:
        paginated_que = paginator.page(page)

    except PageNotAnInteger:
        paginated_que = paginator.page(1)

    except EmptyPage:
        paginated_que = paginator.page(paginator.num_pages)


    
    # answers = Answer.objects.filter(question=questions,reply=None).order_by('-id')

    answers = Answer.objects.filter(question=questions,reply=None).annotate(like_count = Count('like_answer')).order_by('-mark_best')

    answer_count = Answer.objects.filter(question=questions) #count the answers

    q_id = questions #count the number of views
    # print('q id',q_id_up.id)
    # q_id = Question.objects.get(id=q_id_up.id)
    q_id.views += 1
    q_id.save()
    # q_id.

    # print("answeerrr=",answers)
    

    # like = Like.objects.get(id = questions)
    # if like.is_read = False:


    
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST or None)
        if answer_form.is_valid():
            answer = request.POST.get('answer')
            
            user_first = NormalUser.objects.get(user = request.user)
            reply_id = request.POST.get('answer_id')
            reply_qs = None
            if reply_id:
                reply_qs = Answer.objects.get(id = reply_id)
            answer = Answer.objects.create(question=questions, user_a=user_first, answer=answer,reply=reply_qs)
            answer.save()

            '''
            ############## notifications to user ##########
            '''
            notification = Notifications.objects.create(user = user_first,question = questions)
            # notification.save()

            #send the signals



            # return redirect('forumapp:questiondetail', pk=pk)
            return HttpResponseRedirect(questions.get_absolute_url())

            

            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        answerform= AnswerForm()

    context = {
        'questions': questions,
        'answers':answers,
        'answerform1':answerform,
        # 'is_liked': is_liked,
        'answer_count':answer_count,
        'similar_questions':similar_questions,
        'paginated_que':paginated_que,
        # 'max_likes':max_likes

        
    }
    # if request.is_ajax():
    #     html = render_to_string('forum/comment.html', context, request=request)
    #     return JsonResponse({'form': html})
    

    return render(request, 'question/questiondetails.html', context)



"""
question liked
"""
@login_required(login_url='/login/user/')
def LikeView(request):
    user = request.user

    if request.method == "POST":
        q_id = request.POST.get('q_id')
        # q_id = get_object_or_404(Question, id=request.POST.get('question_id'))

        question = Question.objects.get(id=q_id)
        if user in question.like_question.all():
            question.like_question.remove(user)
        else:            
            question.like_question.add(user)
            question.save()
        user = request.user
        normal_user = NormalUser.objects.get(user = user)

        like,created = Like.objects.get_or_create(user = user,question_id = q_id) 
        
        ######notify users when somone liked questions#####
        # liked_notification = Like.objects.get(user = user)
        # print('liked_notification = ',liked_notification)


        # notify = Notifications.objects.create(question_id = q_id,like = liked_notification)
        # print('notify = ',notify)
        # notify.save()
        if not created:
            if like.value == "like":
                like.value == "unlike"
            else:
                like.value == "like"
        like.save()


    # return HttpResponseRedirect(q_id.get_absolute_url())

    return redirect('forumapp:home')
    
        # questions.like_question.add(True)




"""
answer liked
"""
@login_required(login_url='/login/user/')
def LikeAnswerView(request):
    user = request.user
    # question = Answer.objects.get(question_id = )
    if request.method == "POST":

        question_id = request.POST.get('question_id')
        a_id = request.POST.get('a_id')
        markbest_id = request.POST.get('markbest_id')
        print("mark best id",markbest_id)
        print("a id id",a_id)


        if a_id:
            answer = Answer.objects.get(id=a_id)
            if user in answer.like_answer.all():
                answer.like_answer.remove(user)
            else:            
                answer.like_answer.add(user)
                answer.save()
            like,created = Like.objects.get_or_create(user = user,answer_id = a_id) 
            if not created:
                if like.value == "like":
                    like.value == "unlike"
                else:
                    like.value == "like"
            like.save()
        else:
            return None

    # return HttpResponseRedirect(request.path_info)
    return redirect(reverse('forumapp:questiondetail', kwargs={'pk': question_id}))

    

@login_required(login_url='/login/user/')
def AcceptAnswerView(request):
    question_id = request.POST.get('question_id')
    print("question id",question_id)
    # question = Answer.objects.get(question_id = )
    if request.method == "POST":
        answer_id = request.POST.get('markbest_id',None)
        print("mark best id",answer_id)
        answer = Answer.objects.get(id=answer_id)
        if answer.mark_best is False:
            answer.mark_best = True
            answer.save()
        else:
            answer.mark_best = False
            answer.save()
    return redirect(reverse('forumapp:questiondetail', kwargs={'pk': question_id}))



   



"""
Answer update
"""
class AnswerUpdateView(UpdateView):
    template_name = 'answer/answerupdate.html'
    model = Answer
    form_class = AnswerForm
    # success_url = reverse_lazy("forumapp:home")

     ##### render to the page after update #########
        ##### render to the page after delete #########
    def get_success_url(self, **kwargs):
        return reverse_lazy('forumapp:questiondetail', kwargs={'pk': self.object.question.pk})


       


"""
answer delete
"""
class AnswerDeleteView(DeleteView):
    template_name = 'answer/answerdelete.html'
    model = Answer
    success_message = 'Success: Answer was deleted.'

    success_url = reverse_lazy("forumapp:home")

    ##### render to the page after delete #########
    def get_success_url(self, **kwargs):
        
        return reverse_lazy('forumapp:questiondetail', kwargs={'pk': self.object.question.pk})

       

    
"""
show notifications

"""

class NotificationListView(ListView):
    template_name = "notification/notification.html"
    queryset = Notifications.objects.all()
    print("queeryset",queryset)
    context_object_name = 'notifications'
    paginate_by = 10

    # def get_queryset(self):
    #     user = NormalUser.objects.get(user = self.request.user)
    #     print('user = ',user)
    #     return super().get_queryset().filter(user=user)  



"""
Searching questions
"""
# search view 
def SearchView(request):
    print('this is search')
    q = request.GET.get('q')
    if q is not None:       
        # results = Question.objects.filter(Q(question__icontains = q))     
        results = Question.objects.filter(Q(question__icontains=q))     

    return render(request,'search/searchquestion.html', {'results': results})

"""
logout
"""
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/user/')


"""
category education
"""
class CategoryEducationView(TemplateView):
    template_name = 'category/categorylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = Question.objects.filter(category = "education")[:4]    
        return context
    # if pagination is desired
    # def get_queryset(self):
    #     return Question.objects.filter(category=self.kwargs['category_id'])[:4]
    

"""
category sports
"""
class CategorySportsView(TemplateView):
    template_name = 'category/categorylist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sports'] = Question.objects.filter(category = "sports")[:4]    
        return context


"""
category politics
"""
class CategoryPoliticsView(TemplateView):
    template_name = 'category/categorylist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['politics'] = Question.objects.filter(category = "politics")[:4]    
        return context


"""
category fashion and style
"""
class CategoryFashionView(TemplateView):
    template_name = 'category/categorylist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fashion'] = Question.objects.filter(category = "fashion and style")[:4]    
        return context


"""
category health
"""
class CategoryHealthView(TemplateView):
    template_name = 'category/categorylist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['health'] = Question.objects.filter(category = "Health")[:4]    
        return context


"""
CategoryItView
"""
class CategoryItView(TemplateView):
    template_name = 'category/categorylist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['it'] = Question.objects.filter(category = "Information and technology")[:4]    
        return context






class QuestionView(TemplateView):
    template_name = 'user/questionview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = NormalUser.objects.all()    
        context['answers'] = Answer.objects.all()
        context['questions'] = Question.objects.all().order_by("-id")[:15]
        return context
    

class UserView(TemplateView):
    template_name = 'user/userview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = NormalUser.objects.all()    
        return context



"""
question update
"""
class QuestionUpdateView(UpdateView):
    print('ram is gud boy')
    template_name = 'question/questionupdate.html'
    model = Question
    form_class = QuestionUpdateForm
    # success_url = reverse_lazy("forumapp:home")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        q_id = self.kwargs['pk']
        print("question set q_id",q_id)

        question = Question.objects.get(id=q_id)
        print("question set",question)
        today_date = datetime.datetime.now()
        question.date_updated = today_date
        question.questions_updated = True
        question.save()
        return context

     ##### render to the page after update #########
    def get_success_url(self, **kwargs):
        print("keargs",**kwargs)
        return reverse_lazy('forumapp:home')



"""
question delete
"""
class QuestionDeleteView(DeleteView):
    template_name = 'question/questiondelete.html'
    model = Question
    success_message = 'Success: question was deleted.'

    ##### render to the page after delete #########
    def get_success_url(self, **kwargs):
        
        return reverse_lazy('forumapp:home')

###-------------------------------- Admin section start --------------------------####
class AdminHome(TemplateView):
    template_name = "admintemplates/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        context['users'] = User.objects.all()
        #category
        category = []
        question_list = Question.objects.all()
        for item in question_list:
            category.append(item.category)

        # ram = set(category)
        context['pol'] = category.count("politics")
        context['fas'] = category.count("fashion and style")
        context['edu'] = category.count("education")
        context['hea'] = category.count("Health")
        context['inf'] = category.count("Information and technology")
        context['spo'] = category.count("sports")
        print("polll",context['pol'])
        return context



class UserDeleteView(SuccessMessageMixin,DeleteView):
    """
    user delete
    """
    template_name = 'admintemplates/user-delete.html'
    model = NormalUser
    success_url = reverse_lazy("forumapp:userview")
    success_message = 'User has been successfully  deleted.'


class QuestionAdminDeleteView(SuccessMessageMixin,DeleteView):
    """
    Question delete
    """
    template_name = 'admintemplates/admin-question-delete.html'
    model = Question
    success_url = reverse_lazy("forumapp:questionview")
    success_message = 'Question has been successfully  deleted.'


