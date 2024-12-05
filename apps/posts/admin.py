from django.contrib import admin

from .models import Post, Image


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "upvotes", "downvotes"]
    list_filter = ["author", ]
    search_fields = ["title", ]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["image", "post", "author"]
    search_fields = ["post__title", "post__slug", "post__author__email"]


admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
