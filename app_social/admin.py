from django.contrib import admin
from app_social.models import Like, Bookmark, Comment, CommentLike


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'content_object',
    )


class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'content_object',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('value', 'approved', 'content_object')
    search_fields = ('value', )
    list_filter = ('approved', 'content_type', )

admin.site.register(Like, LikeAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike)
