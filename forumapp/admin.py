from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user_q','question','date_created','date_updated','views')


admin.site.register(Question,QuestionAdmin)
admin.site.register([NormalUser,Answer,Comment,Like,Notifications])