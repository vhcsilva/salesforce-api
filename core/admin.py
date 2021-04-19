from django.contrib import admin
from django.contrib.auth.models import Permission

from core.models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Permission)
