
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.views.generic import *
from .forms import UserForm,LoginForm,QuestionForm,AnswerForm,QuestionLikeForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView
# Create your views here.


"""
Homepage

"""
class HomeView(TemplateView):
    template_name = 'forum/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        print(context['questions'],'*****')
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
        print('this is form')
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        print('uname= ',uname)
        user = User.objects.create_user(uname,pword)
        form.instance.user = user
        # messages.info(request,'Profile details updated.')
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
                return HttpResponseRedirect(reverse('forumapp:home'))
        else:
            return render(request,'user/login.html',{
                'messages': 'your username doesnot exist',
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
        form.instance.normal_user = question_user
        return super().form_valid(form)


"""
details of question

"""


def QuestionDetailView(request,pk):
    print('fbv')
    questions = get_object_or_404(Question,pk=pk)
    is_liked = False

    # print("questions is read",questions.is_read)  
    if questions.like_question.filter(id=request.user.id).exists():
        print("this is if in question detail view")
        questions.like_question.remove(request.user)
        is_liked = True


   
    answers = Answer.objects.filter(question=questions,reply=None).order_by('-id')
    # print("answeerrr=",answers)
    

    # like = Like.objects.get(id = questions)
    # if like.is_read = False:


    
    if request.method == 'POST':
        print('appear only after form submitted')
        answer_form = AnswerForm(request.POST or None)
        if answer_form.is_valid():
            answer = request.POST.get('answer')
            print('%%%%%%%%%%%%%%%%%%',request.user)
            user_first = NormalUser.objects.get(user = request.user)
            print(user_first,'@@@@@@@@@@@@@')
            reply_id = request.POST.get('answer_id')
            print('reply id',reply_id)
            reply_qs = None
            if reply_id:
                reply_qs = Answer.objects.get(id = reply_id)
                print('reply_qs = ',reply_qs)
            answer = Answer.objects.create(question=questions, user=user_first, answer=answer,reply=reply_qs)
            print('asnwer',answer)
            answer.save()
            # return redirect('forumapp:questiondetail', pk=pk)
            return HttpResponseRedirect(questions.get_absolute_url())

            

            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        answerform= AnswerForm()

    context = {
        'questions': questions,
        'answers':answers,
        'answerform1':answerform,
        'is_liked': is_liked,

        
    }
    # if request.is_ajax():
    #     html = render_to_string('forum/comment.html', context, request=request)
    #     return JsonResponse({'form': html})
    

    return render(request, 'question/questiondetails.html', context)



"""
question liked
"""
def LikeView(request):
    print('this is like view')
    # questions = get_object_or_404(Question,pk=pk)

    
    questions = get_object_or_404(Question, id=request.POST.get('question_id'))
    print('questions = ######',questions)
    print('questions = ######',questions.id)

    is_liked = False

    if questions.like_question.filter(id = request.user.id).exists():
        print('this is like in if')

        questions.like_question.remove(request.user)
        is_liked = False
    else:
        print('this is like in else')
        # questions.like_question.username = request.user
        # questions.is_read = True
        # questions.save()
        user = User.objects.get(id = request.user.id)
        print('user =',user)
        print('user = ',user)
        # user.question_set.add(questions)
        questions.like_question.add(request.user)

        # q1 = questions.like_question.add(user)
        print('q1 = ',questions)
        print('q1 = ',questions.id)

        print('q1 = ',questions.like_question.all())

        # questions.like_question.add(user)
        # print('many ti many field at last = ',questions.id)
        # print('many ti many field at last = ',questions.like_question.all())
        # q1.save()



        # task.users.add(form.cleaned_data['user'])
        # questions.like_question.set(user)
        


        # questions.save()


        is_liked = True
    return HttpResponseRedirect(questions.get_absolute_url())

    # return redirect('forumapp:questiondetail', pk=pk)
    
        # questions.like_question.add(True)






    # user = request.user
    # like_created = Like.objects.create(question = questions_id,user = user,is_read = True)
    # print("like created",like_created)

   








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