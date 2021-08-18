# Register your models here.
from django.contrib.auth import admin
from django.contrib import admin
from api.models import Profile, Organization

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile)

class OrganizationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Organization)