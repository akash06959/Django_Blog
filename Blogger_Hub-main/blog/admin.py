from django.contrib import admin
from .models import Post, UserProfile, Comment

# Register your models here.
admin.site.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('content', 'author__username', 'post__title')
