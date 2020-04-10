
from django.shortcuts import render,redirect,reverse
from django.views.generic import *
from .forms import UserForm,LoginForm,QuestionForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'forum/home.html'


####################### login form ###############
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



#sign up view
class RegisterView(CreateView):
    template_name = 'user/userlogin.html'
    form_class = UserForm
    success_url = reverse_lazy('forumapp:login')
    print('this is upper')

    def form_valid(self, form):
        print('this is form')
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        print('uname= ',uname)
        user = User.objects.create_user(uname,pword)
        form.instance.user = user
        # messages.info(request,'Profile details updated.')
        return super().form_valid(form)



#login form
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
    
class QuestionAddView(BSModalCreateView):
    print('i have great')
    template_name = "question/questioncreate.html"
    form_class = QuestionForm
    print('below form class')
    success_message = "Question has been added"
    print('this is below success')
    success_url = reverse_lazy('forumapp:home')
    print('888888')


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



# def QuestionCreateView(request):
#     if request.method == 'GET':
#         form = QuestionForm
#         category = Category.objects.all()
#         # print(customerform,"88888")
#         return render(request, 'question/questioncreate.html',{'category':category , 'form':form})
#     else:
#         catgry = request.POST.get('dropdown',None)
#         print(cid,'|||||||||||||')
#         customer = NormalUser.objects.get(=catgry)
#         products = list(Product.objects.all())
#         if customer is not None:
#             return render(request, 'sales/test.html', {'customer': customer, 'products': products})
#         else:
#             return messages.error(request, "Error!")