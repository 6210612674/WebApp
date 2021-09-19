from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import *

class RegAdmin(admin.ModelAdmin):
    list_display = ("course_code", "course_name", "course_status", "course_quota")
    filter_horizontal = ("students",)


admin.site.register(Reg, RegAdmin)
