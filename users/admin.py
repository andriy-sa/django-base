from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class Admin(admin.ModelAdmin):
    pass

admin.site.register(models.MyUser,UserAdmin)
