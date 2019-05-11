import jdatetime
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Chat(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True)
    code = models.TextField(null=True, blank=True)
    message = models.TextField(null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    seen = models.BooleanField(null=True, default=False)
    seen_datetime = models.DateTimeField(null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def jd_create_datetime(self):
        jdatetime.set_locale('fa_IR')
        jdatetime.datetime.now().strftime('%A %B')
        jd_datetime = jdatetime.datetime.fromgregorian(
            year=self.create_datetime.year,
            month=self.create_datetime.month,
            day=self.create_datetime.day,
            hour=self.create_datetime.hour,
            monute=self.create_datetime.minute,
            second=self.create_datetime.second,
        )
        return jd_datetime.strftime('%A, %d %B %y %H:%M:%S')

    def status_color(self):
        return 'grey' if self.seen else 'teal'

    def status(self):
        return 'دیده شده' if self.seen else 'دیده نشده'

    def is_done_exercise(self):
        return self.group.content_object in [e.exercise for e in self.group.user.exercisebystudent_set.all()]

    def done_color(self):
        return 'teal' if self.is_done_exercise() else 'red'

    def done_status(self):
        return 'انجام شده' if self.is_done_exercise() else 'انجام نشده'

    def is_student(self):
        return 'students' in [group.name for group in self.group.user.groups.all()]

    def is_operator(self):
        return not self.is_student()

    def __str__(self):
        return self.message[:30]


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=60, null=True)
    chats = GenericRelation(Chat, null=True)
    closed = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(default=timezone.now, blank=True)

    def status(self):
        return 'بسته' if self.closed else 'باز'

    def status_color(self):
        return 'red' if self.closed else 'blue'

    def jd_create_datetime(self):
        self.create_datetime = localtime(self.create_datetime)
        jdatetime.set_locale('fa_IR')
        jdatetime.datetime.now().strftime('%A %B')
        jd_datetime = jdatetime.datetime.fromgregorian(
            year=self.create_datetime.year,
            month=self.create_datetime.month,
            day=self.create_datetime.day,
            hour=self.create_datetime.hour,
            minute=self.create_datetime.minute,
            second=self.create_datetime.second,
        )
        return jd_datetime.strftime('%A, %d %B %y %H:%M:%S')

    def get_absolute_url(self):
        params = {'id': self.id}
        return reverse('app-accounts:ticket-detail', kwargs=params)

    def __str__(self):
        return self.topic
