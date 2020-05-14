
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.views.generic import *
from .forms import UserForm,LoginForm,QuestionForm,AnswerForm,QuestionLikeForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView
from django.db.models import Count
from .signals import new_comment
# Create your views here.


"""
Homepage

"""
class HomeView(TemplateView):
    template_name = 'forum/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        context['answers'] = Answer.objects.all()

        # context['answer-count'] = Question.objects.annotate(number_of_answers=Count('answer'))

        print(context['questions'],'*****')
        # context['profile'] = NormalUser.objects.get(id = self.request.user.id)
        context['form'] = AnswerForm()
        
        
        return context

        # {% if question.image %}<div class="user"><img src="{{ question.normal_user.image.url }}"></div>{% endif %} 

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
        print("pword",pword)
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
        print("user = ",user)
        if user:
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('forumapp:home'))
        else:
            return render(request,'user/login.html',{
                'messages': 'your username doesnot exist 11',
                'form': LoginForm
            })
            # return HttpResponse("your username did not match")
    
    else:
        form = LoginForm
        print(form)
        return render(request,'user/login.html',{'form':form})
    



"""
Question add

"""
class QuestionAddView(BSModalCreateView):
    template_name = "question/questioncreate.html"
    form_class = QuestionForm
    success_message = "Question has been added"
    success_url = reverse_lazy('forumapp:home')

    def form_valid(self,form):
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&77')
        usr = self.request.user
        print('user = ',usr)
        # catgry = self.request.get('dropdown',None)
        # print('catgru=',catgry)
        # category = Category.objects.get(name=catgry)
        # form.instance.category = category
        question_user = NormalUser.objects.get(user = usr)
        print('question user',question_user)
        form.instance.user_q = question_user
        return super().form_valid(form)

    # def form_valid(self,form):
    #     print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&77')
    #     usr = self.request.user
    #     print('user = ',usr)
    #     # catgry = self.request.get('dropdown',None)
    #     # print('catgru=',catgry)
    #     # category = Category.objects.get(name=catgry)
    #     # form.instance.category = category
    #     user1 = User.objects.get(id=usr.id)
    #     print('user1',user1)
    #     question_user = NormalUser.objects.get(user_id = user1)
    #     print('question user',question_user)
    #     form.instance.user_a = question_user
    #     return super().form_valid(form)


"""
details of question

"""


def QuestionDetailView(request,pk):
    print('fbv')
    questions = get_object_or_404(Question,pk=pk)
    print('sakalalalalala',questions.id)
    print('sakalalalalala count',questions.like_question)

    answers = Answer.objects.filter(question=questions,reply=None).order_by('-id')

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
        print('appear only after form submitted')
        answer_form = AnswerForm(request.POST or None)
        if answer_form.is_valid():
            answer = request.POST.get('answer')
            
            print('%%%%%%%%%%%%%%%%%%',request.user.id)
            user_first = NormalUser.objects.get(user = request.user)

            print(user_first,'@@@@@@@@@@@@@')
            reply_id = request.POST.get('answer_id')
            print('reply id',reply_id)
            reply_qs = None
            if reply_id:
                reply_qs = Answer.objects.get(id = reply_id)
                print('reply_qs = ',reply_qs)
            answer = Answer.objects.create(question=questions, user_a=user_first, answer=answer,reply=reply_qs)
            print('asnwer',answer)
            answer.save()

            '''
            ############## notifications to user ##########
            '''
            notification = Notifications(user = user_first,question = questions)
            notification.save()

            #send the signals
            new_comment.send(sender = notification,user = user_first,question = questions) 



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

        
    }
    # if request.is_ajax():
    #     html = render_to_string('forum/comment.html', context, request=request)
    #     return JsonResponse({'form': html})
    

    return render(request, 'question/questiondetails.html', context)



"""
question liked
"""
def LikeView(request):
    user = request.user
    if request.method == "POST":
        q_id = request.POST.get('q_id')
        print("questio i d ",q_id)
        # q_id = get_object_or_404(Question, id=request.POST.get('question_id'))

        print('b idididid',q_id)
        question = Question.objects.get(id=q_id)
        print('type og question',type)


        if user in question.like_question.all():
            question.like_question.remove(user)
        else:            
            question.like_question.add(user)
            print('blog liked',question.like_question)
            question.save()
        like,created = Like.objects.get_or_create(user = user,question_id = q_id) 
        ######notify users when somone liked questions#####
        liked_notification = Like.objects.get(id = user.id)
        print('liked_notification = ',liked_notification)


        notify = Notifications.objects.create(question_id = q_id,like = liked_notification)
        print('notify = ',notify)
        notify.save()
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
def LikeAnswerView(request):
    print('this is answer like view')
    user = request.user
    # question = Answer.objects.get(question_id = )
    if request.method == "POST":

        question_id = request.POST.get('question_id')
        print("this is question id buddha jayanti",question_id)
        a_id = request.POST.get('a_id')
        print("questio i d ",a_id)
        # q_id = get_object_or_404(Question, id=request.POST.get('question_id'))

        print('b idididid',a_id)
        answer = Answer.objects.get(id=a_id)
        print('type og question',type)


        if user in answer.like_answer.all():
            answer.like_answer.remove(user)
        else:            
            answer.like_answer.add(user)
            print('blog liked',answer.like_answer)
            answer.save()
        like,created = Like.objects.get_or_create(user = user,answer_id = a_id) 
        if not created:
            if like.value == "like":
                like.value == "unlike"
            else:
                like.value == "like"
        like.save()

    # return HttpResponseRedirect(request.path_info)
    return redirect(reverse('forumapp:questiondetail', kwargs={'pk': question_id}))

    # return HttpResponseRedirect(a_id.get_absolute_url())

    # return redirect('forumapp:home')
    




    # user = request.user
    # like_created = Like.objects.create(question = questions_id,user = user,is_read = True)
    # print("like created",like_created)

   



"""
Answer update
"""
class AnswerUpdateView(UpdateView):
    print('this is answer update')
    template_name = 'answer/answerupdate.html'
    model = Answer
    form_class = AnswerForm
    # success_url = reverse_lazy("forumapp:home")

     ##### render to the page after update #########
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
    template_name = "forum/notification.html"
    queryset = Notifications.objects.all()
    print("queeryset",queryset)
    context_object_name = 'notifications'
    paginate_by = 10

    # def get_queryset(self):
    #     user = NormalUser.objects.get(user = self.request.user)
    #     print('user = ',user)
    #     return super().get_queryset().filter(user=user)  






##################### class based views #############
'''
class QuestionDetailView(DetailView):
    template_name = 'question/questiondetails.html'
    
    model = Question
    context_object_name = 'questions'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.object.pk)
        context['answerform'] = AnswerForm()
        print(context['answerform'],'******************')

        print(context['answers'],'******************')
        print('pk=',self.object.pk)
        return context
    
    ############form validation ############
    def form_valid(self,form):
        print('this is form valid method')
        new_answer = form.cleaned_data['answer']
        answer = Answer.objects.create(question=self.object.pk,user=self.request.user,answer=new_answer)
        form.instance.answer = answer
        return super().form_valid(form)

'''