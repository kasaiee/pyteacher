from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from app_base.models import Course, CourseSession
from django.core.exceptions import ValidationError
from datetime import datetime
from jdatetime import datetime as jd
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()


EDUCATION_TYPES = (
    (1, 'دانش‌آموزش'),
    (2, 'دیپلم'),
    (3, 'دانشجو'),
    (4, 'کاردانی'),
    (5, 'کارشناسی'),
    (6, 'کارشناسی ارشد'),
    (7, 'دکتری'),
)


def check_education(value):
    if not (1 <= value <= 7):
        raise ValidationError('در انتخاب سطح تحصیلات دقت نمائید!')


def avatar_path(instance, filename):
    return '%s/%s' % (instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('درباره من', max_length=500, blank=True)
    _education = models.PositiveSmallIntegerField('تحصیلات', choices=EDUCATION_TYPES, null=True, blank=True, validators=[check_education])
    phone = models.CharField('شماره همراه', max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)
    show_resume = models.BooleanField(default=False)

    @property
    def jbirth_date(self):
        return jd.fromgregorian(
            year=self.birth_date.year,
            month=self.birth_date.month,
            day=self.birth_date.day)

    @jbirth_date.setter
    def jbirth_date(self, value):
        if type(value) == str:
            self.birth_date = jd.strptime(value, '%Y-%m-%d')
        elif type(value) == jd:
            self.birth_date = jd.togregorian(value)

    @property
    def education(self):
        return dict(EDUCATION_TYPES)[self._education]

    @education.setter
    def education(self, education_type):
        reversed_types = {v: k for k, v in dict(EDUCATION_TYPES).items()}
        self._education = reversed_types.get(education_type)

    def save(self, *args, **kwargs):
        if type(self.birth_date) == datetime:
            self.birth_date = self.birth_date.strftime('%Y-%m-%d')
        super().save(*args, **kwargs)
        if not self.user.is_superuser:
            Group.objects.get(name='students').user_set.add(self.user)

    def registered_items(self):
        return [item.course if item.course else item.session for item in self.user.registereditem_set.all()]

    def registered_sessions(self):
        return [i for i in self.registered_items() if hasattr(i, 'course')]

    def registered_courses(self):
        return [i for i in self.registered_items() if hasattr(i, 'session')]

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.profile._education:
        instance.profile._education = 0
    instance.profile.save()


class RegisteredItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, null=True)

    def item(self):
        if self.course:
            return self.course
        else:
            return self.session

    def __str__(self):
        if self.course:
            return '%s - %s' % (self.user.username, self.course.title)
        elif self.session:
            return '%s - %s' % (self.user.username, self.session.title)
        else:
            return '?'
