from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([NormalUser,Category,Question,Answer,Comment,Report])