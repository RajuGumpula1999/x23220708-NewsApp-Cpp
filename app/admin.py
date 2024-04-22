from django.contrib import admin
from .models import *

@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_date", "updated_date", "user"]

