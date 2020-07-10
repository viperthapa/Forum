from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
# Register your models here.
@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

admin.site.register([NormalUser,Category,Answer,Comment,Like,Notifications])