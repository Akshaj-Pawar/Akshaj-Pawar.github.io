from django.contrib import admin
from firstapp.models import Posts, Comment


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


admin.site.register(Posts, PostsAdmin)
admin.site.register(Comment)