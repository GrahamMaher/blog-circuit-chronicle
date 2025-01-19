from django.contrib import admin
from .models import UserProfile, Category, Tag, Post, Comment, NewsletterSubscription, ContactMessage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'approved', 'created_on')
    list_filter = ('approved', 'created_on')
    search_fields = ('author__username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsletterSubscription)
admin.site.register(ContactMessage)