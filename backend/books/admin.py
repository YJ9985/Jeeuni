from django.contrib import admin
from .models import Category, Book, Post, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Post)
admin.site.register(Comment)
