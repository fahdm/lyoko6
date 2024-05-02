from django.contrib import admin
from .models import Category, Comment, Post
# Register your models here.

admin.site.register ([Category,Comment,Post])