from django.contrib import admin
from app_base.models import (
    Course,
    CourseSession,
    CourseSessionExercise,
    ExerciseByStudent,
    AttachmentFiles,
    ExerciseReply,
)
from genericadmin.admin import GenericAdminModelAdmin, GenericTabularInline



class ExerciseReplyInline(admin.StackedInline):
    model = ExerciseReply


class AttachmentsInline(GenericTabularInline):
    model = AttachmentFiles


class CourseSessionAdmin(GenericAdminModelAdmin):
    list_filter = ('price', 'course')
    inlines = [
        AttachmentsInline,
    ]


class CourseSessionExerciseAdmin(GenericAdminModelAdmin):
    list_filter = ('course_session__course', )
    inlines = [
        AttachmentsInline,
        ExerciseReplyInline,
    ]


admin.site.register(Course)
admin.site.register(CourseSession, CourseSessionAdmin)
admin.site.register(CourseSessionExercise, CourseSessionExerciseAdmin)
admin.site.register(ExerciseByStudent)
admin.site.register(AttachmentFiles)
