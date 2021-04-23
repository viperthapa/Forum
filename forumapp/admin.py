from django.contrib import admin

# Register your models here.
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user_q','question','date_created','date_updated','views')


admin.site.register(Question,QuestionAdmin)
admin.site.register([NormalUser,Answer,Comment,Like,Notifications])