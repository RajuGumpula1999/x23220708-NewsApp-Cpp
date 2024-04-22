from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from django.contrib.auth.models import User

class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="blog_image")
    content = RichTextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100, null=True, blank=True, default="Anonymous author")
