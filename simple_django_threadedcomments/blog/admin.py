from django.contrib import admin
from .models import Post, ThreadedComment


class PostAdmin(admin.ModelAdmin):
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)


class ThreadedCommentAdmin(admin.ModelAdmin):
    class Meta:
        model = ThreadedComment

admin.site.register(ThreadedComment, ThreadedCommentAdmin)