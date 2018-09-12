from django.contrib import admin

# Register your models here.
from .models import *
# from django.contrib.auth.models import auth
admin.site.register(UserProfile)
admin.site.register(MenuInfo)
admin.site.register(RoleInfo)

# admin.site.register(auth)
