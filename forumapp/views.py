
from django.shortcuts import render,redirect,reverse
from django.views.generic import *
from .forms import UserForm,LoginForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.


class HomeView(TemplateView):
    template_name = 'forum/home.html'



class TestView(TemplateView):
    template_name = "forum/test.html"
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
    

# class RegisterView(CreateView):
#     template_name = 'forum/test.html'
#     print('hshshshsh')
#     form_class = UserForm
#     print('8888')
#     success_url = reverse_lazy('forumapp:home')

#     def form_valid(self, form):
#         u_name = form.cleaned_data['username']
#         pword = form.cleaned_data['password']
#         # email = form.cleaned_data['email']

#         user = User.objects.create_user(u_name,pword)
#         form.instance.user = user
#         # login(self.request, user)
#         return super().form_valid(form)
