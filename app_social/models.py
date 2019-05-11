from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.content_object.title


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.content_object.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=400, null=True)
    approved = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    comments = GenericRelation('Comment')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        if hasattr(self.content_object, 'title'):
            return '%s - %s' % (self.content_object.title, ' '.join(self.value.split()[:10]))
        else:
            return ' '.join(self.value.split()[:10])


class CommentLike(models.Model):
    LIKE_TYPES = (
        (1, 'میپسندم!'),
        (-1, 'نمیپسندم!'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    value = models.SmallIntegerField(null=True, choices=LIKE_TYPES)

    def __str__(self):
        return str(self.value)
