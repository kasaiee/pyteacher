from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import jdatetime
from django.utils.timezone import localtime
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from app_chat.models import ChatGroup
from app_social.models import Like, Bookmark, Comment
from django.contrib.auth import get_user_model
User = get_user_model()


def course_image_path(instance, filename):
    return instance.title


def attachment_path(instance, filename):
    return instance.title


class Course(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=True)
    image = models.ImageField(upload_to=course_image_path, null=True)
    title = models.CharField(max_length=100, null=True)
    description = RichTextUploadingField(null=True)
    chats = GenericRelation(ChatGroup)
    likes = GenericRelation(Like)
    bookmarks = GenericRelation(Bookmark)
    comments = GenericRelation(Comment)

    def price(self):
        return sum([se.price for se in self.coursesession_set.all()]) 

    def get_absolute_url(self):
        params = {'slug': self.slug}
        return reverse('app-base:course-detail', kwargs=params)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


def get_upload_path(instance, filename):
    return 'session/private-videos/%s/%s' % (instance.id, filename)


class CourseSession(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    description = RichTextUploadingField(null=True)
    aparat_video = models.TextField(null=True, blank=True)
    prev_session = models.ForeignKey(
        'CourseSession', on_delete=models.SET_NULL, null=True, related_name='prev', blank=True)
    video = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    attachment_files = GenericRelation('AttachmentFiles')
    chats = GenericRelation(ChatGroup)
    likes = GenericRelation(Like)
    bookmarks = GenericRelation(Bookmark)
    comments = GenericRelation(Comment)
    price = models.PositiveIntegerField(null=True, default=0)

    def next_session(self):
        return CourseSession.objects.get(prev_session=self)

    @property
    def has_price(self):
        return boll(self.price)

    def image(self):
        return self.course.image

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        params = {'course_slug': self.course.slug, 'session_slug': self.slug}
        return reverse('app-base:course-session-detail', kwargs=params)

    def __str__(self):
        return self.title


class CourseSessionExercise(models.Model):
    slug = models.SlugField(null=True, allow_unicode=True, blank=True)
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    description = RichTextUploadingField(null=True)
    aparat_video = models.TextField(null=True, blank=True)
    attachment_files = GenericRelation('AttachmentFiles')
    chats = GenericRelation(ChatGroup)
    likes = GenericRelation(Like)
    bookmarks = GenericRelation(Bookmark)
    comments = GenericRelation(Comment)

    def image(self):
        return self.course_session.course.image

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        params = {'course_slug': self.course_session.course.slug,
                  'session_slug': self.course_session.slug, 'exercise_slug': self.slug}
        return reverse('app-base:course-session-exercise-detail', kwargs=params)

    def get_absolute_student_reply_url(self, student_id):
        params = {
            'course_slug': self.course_session.course.slug,
            'session_slug': self.course_session.slug,
            'exercise_slug': self.slug,
            'student_id': student_id
        }
        return reverse('app-base:course-session-exercise-detail-with-reply', kwargs=params)

    def user(self):
        if self.chats.first():
            return [c.user for c in self.chats.all() if not c.user.is_superuser][0]

    def __str__(self):
        return self.title + ' - ' + self.course_session.title + ' - ' + self.course_session.course.title


class ExerciseReply(models.Model):
    exercise = models.ForeignKey(CourseSessionExercise, on_delete=models.CASCADE, null=True)
    code = models.TextField()

    def __str__(self):
        return '%s: تمرین %s ' % (self.id, self.exercise.title)


class ExerciseByStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(CourseSessionExercise, on_delete=models.CASCADE, null=True)
    # rate = models.PositiveSmallIntegerField(null=True)
    done = models.BooleanField(default=True)
    code = models.TextField(null=True, blank=True)
    done_datetime = models.DateTimeField(auto_now_add=True, null=True)

    def jd_done_datetime(self):
        self.done_datetime = localtime(self.done_datetime)
        jdatetime.set_locale('fa_IR')
        jdatetime.datetime.now().strftime('%A %B')
        jd_datetime = jdatetime.datetime.fromgregorian(
            year=self.done_datetime.year,
            month=self.done_datetime.month,
            day=self.done_datetime.day,
            hour=self.done_datetime.hour,
            minute=self.done_datetime.minute,
            second=self.done_datetime.second,
        )
        return jd_datetime.strftime('%A, %d %B %y %H:%M:%S')

    def __str__(self):
        return self.user.username + ' ' + self.exercise.title


class AttachmentFiles(models.Model):
    file = models.FileField(upload_to='attach-files/%y-%m-%d_%H:%M')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def title(self):
        return self.file.url.split('/')[-1]

    @property
    def color(self):
        colors = {
            'ppt': 'orange',
            'pptx': 'orange',
            'doc': 'light-blue darken-3',
            'docx': 'light-blue darken-3',
            'csv': 'green',
            'xlsx': 'green',
            'xls': 'green',
            'py': 'yellow',
            'pdf': 'pink',
        }
        file_format = self.title.split('.')[-1]
        return colors.setdefault(file_format, 'grey')

    def __str__(self):
        return self.content_object.title
