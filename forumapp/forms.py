from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


#register form
class UserForm(forms.ModelForm):
    fname= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your first name'}))
    lname= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your last name'}))
    email= forms.EmailField(widget= forms.EmailInput(attrs={'placeholder':'Enter your email'}))
    username= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password= forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    confirm_password= forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter confirm password'}))

    # username = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'username'}))
    # password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'password'}))
    # confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
    # fname = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'first name'}))
    # lname = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'last name'}))
    # email = forms.CharField(widget = forms.EmailField(attrs={'placeholder': 'enter email'}))


    class Meta:
        model = NormalUser
        fields = ['fname','lname','email','username','password','confirm_password']

    #check the username 
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username = username)
        if user.exists():
            raise forms.ValidationError("username already exist")
        return username
    
    #check the password match
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:

            raise forms.ValidationError("password didnot match")
        return confirm_password




#login form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'})) 

#question asked
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category','question']
        widgets = {
            
            'category': forms.Select(attrs={
                'placeholder':"choose",
                'id': "catgory",
                'class': 'form-control',
            }),
            'question': SummernoteWidget(),
            # 'question': SummernoteInplaceWidget(),




        }
