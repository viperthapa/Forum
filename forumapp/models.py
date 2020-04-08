from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.


#Normal user
class NormalUser(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    fname = models.CharField(max_length = 250)
    lname = models.CharField(max_length = 200)
    email = models.EmailField()
    image = models.ImageField(upload_to = 'user')
    date_created = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='normal_user')
        self.user.groups.add(group)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.fname

#category
class Category(models.Model):
    name = models.CharField(max_length = 150)

    def __str__(self):
        return self.name


#question 
class Question(models.Model):
    normal_user = models.ForeignKey(NormalUser,on_delete = models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    question = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='question',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.question


#answer
class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    user = models.ForeignKey(NormalUser,on_delete = models.CASCADE)
    answer = models.TextField()
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)
    upvoted = models.IntegerField(default=0)
    mark_best = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.answer


#comment text
class Comment(models.Model):
    user = models.ForeignKey(NormalUser,on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete = models.CASCADE)
    comment_text = models.TextField(max_length = 800) 
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)

    

    def __str__(self):
        return self.comment_text


#admin
# class Admin(models.Model):
#     admin = models.OneToOneField(User,on_delete = models.CASCADE)

#     def save(self, *args, **kwargs):
#         group, created = Group.objects.get_or_create(name='admin')
#         self.user.groups.add(group)
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return self.admin




class Report(models.Model):
    user = models.ForeignKey(NormalUser,on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete = models.CASCADE)
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    report_name = models.TextField()

    def __str__(self):
        return self.report_name

   






'''
    username = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
    fname = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'first name'}))
    lname = forms.CharField(widget = forms.CharField(attrs={'placeholder': 'last name'}))
    email = forms.CharField(widget = forms.EmailField(attrs={'placeholder': 'enter email'}))

'''