from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm
import django_filters



"""=======================================
-------------Register Form------------------
======================================="""

class UserForm(forms.ModelForm):
    username= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password= forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    confirm_password= forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter confirm password'}))
    fname= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your first name'}))
    lname= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your last name'}))
    email= forms.EmailField(widget= forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    image = forms.ImageField()

    class Meta:
        model = NormalUser
        fields = ['username','password','confirm_password','fname','lname','email','image']

    #check the username 
    def clean_username(self):
        print('this is clean username')
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username = username)
        print("user",user)
        if user.exists():
            print('inside if statemenet')
            raise forms.ValidationError("username already exist")
        return username
    
    #check the password match
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:

            raise forms.ValidationError("password didnot match")
        return confirm_password


    #check the validation of email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Provide a valid email address")
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email already exists")
        return email


"""=======================================
-------------Login Form------------------
======================================="""
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})) 

#question asked




"""=======================================
-------------Question Asked Form------------------
======================================="""
class QuestionForm(forms.Form):
    class Meta:
        model = Question
        fields = ['question']


"""=======================================
-------------Answer Form------------------
======================================="""

class AnswerForm(forms.ModelForm):
    answer = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'post your aswer....', 'rows':'4', 'cols':'50'}))

    class Meta:
        model = Answer
        fields = ('answer',)


"""=======================================
-------------question Form------------------
======================================="""

class QuestionUpdateForm(forms.ModelForm):
    question = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'post your aswer....', 'rows':'4', 'cols':'50'}))

    class Meta:
        model = Question
        fields = ('question',)


"""=======================================
-------------Question Asked Form------------------
======================================="""
class QuestionLikeForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['like_question']


       
"""
Question search
"""
class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['question']