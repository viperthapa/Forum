from django.db import models
from django.contrib.auth.models import User,Group
from django.urls import reverse
from django.dispatch import receiver
from .signals import new_comment
from django.db.models.signals import post_save


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
    user_q = models.ForeignKey(NormalUser,on_delete = models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    question = models.CharField(max_length = 350,null=True)
    like_question = models.ManyToManyField(User, related_name='likes',default=None,blank=True)
    image = models.ImageField(upload_to='question',blank=True)
    description = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)
    views = models.PositiveIntegerField(default=0)

    # is_read = models.BooleanField(default=False)




    def __str__(self):
        return str(self.question)
    
    def num_likes(self):
        return self.like_question.all().count()


    def get_absolute_url(self):
        return reverse("forumapp:questiondetail", args=[self.id])
    



#answer
class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE,related_name="related_question")
    user_a = models.ForeignKey(NormalUser,on_delete = models.CASCADE)
    reply = models.ForeignKey('Answer',null=True,related_name="replies",on_delete = models.CASCADE,blank=True)
    answer = models.TextField()
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)
    mark_best = models.IntegerField(default=0)
    like_answer = models.ManyToManyField(User, related_name='likes_answer',default=None,blank=True)


    def __str__(self):
        return str(self.answer)

    def get_absolute_url(self):
        return reverse("forumapp:questiondetail", args=[self.id])


#comment text
class Comment(models.Model):
    user = models.ForeignKey(NormalUser,on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete = models.CASCADE)
    comment_text = models.TextField(max_length = 800) 
    date_created = models.DateTimeField(auto_now = True)
    date_updated = models.DateTimeField(auto_now = True)

    

    def __str__(self):
        return self.comment_text



'''
add likes
'''
LIKE_CHOICES = ( 
    ("like", "like"), 
    ("Unlike", "Unlike")
) 
class Like(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete = models.CASCADE,null = True,blank = True)
    question = models.ForeignKey(Question,on_delete = models.CASCADE,null = True,blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length = 20,choices = LIKE_CHOICES, default = 'like') 
    # is_read = models.BooleanField(default=False)

    def __str__(self):   
        return self.user.username



'''
Notification to users
'''



class Notifications(models.Model):
    # Actor: The object which performed the activity.
    user = models.ForeignKey(NormalUser, related_name="notify_user", on_delete=models.CASCADE)
    # verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    question = models.ForeignKey(Question,related_name='notify_answers',on_delete=models.CASCADE,null = True,blank = True)
    like = models.ForeignKey(Like,related_name='notification_likes',on_delete=models.CASCADE,null = True,blank = True)

    message = models.TextField()
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.user.user.id)
    

    

















