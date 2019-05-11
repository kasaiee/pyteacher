import jdatetime
from rest_framework import serializers
from app_social.models import Comment, CommentLike
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from app_chat.models import Ticket


class CommentListSerializer(serializers.ModelSerializer):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    replies = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    jcreate_datetime = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dilikes = serializers.SerializerMethodField()

    def get_replies(self, obj):
        return CommentListSerializer(
            instance=obj.comments.filter(approved=True), many=True, user=self.user).data

    def get_avatar(self, obj):
        if obj.user.profile.avatar:
            return get_thumbnail(obj.user.profile.avatar, '55x55', crop='center', quality=99).url
        else:
            return settings.DEFAULT_USER_AVATAR

    def get_user_full_name(self, obj):
        return obj.user.get_full_name() if obj.user.get_full_name() else obj.user.username

    def get_jcreate_datetime(self, obj):
        return jdatetime.datetime.fromgregorian(
            year=obj.create_datetime.year,
            month=obj.create_datetime.month,
            day=obj.create_datetime.day,
            hour=obj.create_datetime.hour,
            minute=obj.create_datetime.minute).strftime('%y-%m-%d %H:%M')

    def get_is_liked(self, obj):
        try:
            comment_like = CommentLike.objects.get(user=self.user, comment=obj)
            if comment_like:
                return comment_like.value
        except CommentLike.DoesNotExist:
            return ''

    def get_likes(self, obj):
        return sum([cl.value for cl in CommentLike.objects.filter(comment=obj) if cl.value == 1])

    def get_dilikes(self, obj):
        return sum([cl.value for cl in CommentLike.objects.filter(comment=obj) if cl.value == -1])

    class Meta:
        model = Comment
        exclude = ('content_type', 'object_id', 'approved', 'user')


class TicketListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    jd_create_datetime = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_jd_create_datetime(self, obj):
        return obj.jd_create_datetime()

    def get_status_color(self, obj):
        return obj.status_color()

    def get_status(self, obj):
        return obj.status()

    class Meta:
        model = Ticket
        exclude = ('create_datetime', )
