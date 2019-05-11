from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from app_chat.models import Ticket
from app_base.models import Course, CourseSession, CourseSessionExercise, ExerciseByStudent
from rest_framework import status
from app_social.models import Comment, CommentLike
from app_api.serializers import CommentListSerializer
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import generics
from app_api.serializers import TicketListSerializer
from rest_framework import filters
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['POST'])
@login_required
def like(request):
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type')
    if obj_id and obj_type:
        if obj_type in settings.ALLOWED_SOCIAL_OBJECTS:
            model = eval(obj_type)
            my_obj = model.objects.get(id=obj_id)
            if my_obj.likes.filter(user=request.user):
                my_obj.likes.filter(user=request.user).delete()
                return Response({"message": "%s دیس لایک شد!" % my_obj.title}, status=status.HTTP_200_OK)
            else:
                my_obj.likes.create(user=request.user)
                return Response({"message": "%s لایک شد!" % my_obj.title}, status=status.HTTP_200_OK)
    return Response({"message": "اوه! یه مشکلی پیش اومده..."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
def bookmark(request):
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type')
    if obj_id and obj_type:
        if obj_type in settings.ALLOWED_SOCIAL_OBJECTS:
            model = eval(obj_type)
            my_obj = model.objects.get(id=obj_id)
            if my_obj.bookmarks.filter(user=request.user):
                my_obj.bookmarks.filter(user=request.user).delete()
                return Response({"message": "%s از نشانه گذاری درآمد!" % my_obj.title}, status=status.HTTP_200_OK)
            else:
                my_obj.bookmarks.create(user=request.user)
                return Response({"message": "%s نشانه گذاری شد!" % my_obj.title}, status=status.HTTP_200_OK)
    return Response({"message": "اوه! یه مشکلی پیش اومده..."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def comment(request):
    if not request.user.is_authenticated:
        return Response(
            {"warning": "برای نظر دادن یا باید وارد سایت بشی یا اینکه ثبت نام کنی!"},
            status=status.HTTP_200_OK)
    comment = request.POST.get('value')
    if not comment:
        return Response(
            {"warning": "فکر کنم یادت رفته نظرتو بگی! لطفا فیلد نظر رو با دقت پر کن..."},
            status=status.HTTP_200_OK)
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type')
    if obj_id and obj_type:
        if obj_type in settings.ALLOWED_SOCIAL_OBJECTS:
            model = eval(obj_type)
            my_obj = model.objects.get(id=obj_id)
            my_obj.comments.create(user=request.user, value=comment)
            return Response(
                {"message": "ممنون که وقت گذاشتی نظر دادی. نظر شما بعد از تائید نمایش داده میشه!"},
                status=status.HTTP_200_OK)
    return Response({"message": "اوه! یه مشکلی پیش اومده..."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comment_list(request):
    obj_id = request.GET.get('id')
    obj_type = request.GET.get('type')
    if obj_id and obj_id.isdigit() and obj_type and obj_type in settings.ALLOWED_SOCIAL_OBJECTS:
        my_model = eval(obj_type)
        try:
            obj = my_model.objects.get(id=obj_id)
        except my_model.DoesNotExist:
            return Response({"message": "این موردی وجود نداره!"}, status=status.HTTP_400_BAD_REQUEST)
        com = Comment.objects.first()
        if com:
            ct = ContentType.objects.get_for_model(com)
            comments = obj.comments.filter(Q(approved=True) & ~Q(content_type=ct))
            serializer = CommentListSerializer(instance=comments, many=True, user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
    return Response({"message": "اوه! یه مشکلی پیش اومده..."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def comment_like(request):
    if not request.user.is_authenticated:
        return Response(
            {"warning": "برای نظر دادن یا باید وارد سایت بشی یا اینکه ثبت نام کنی!"},
            status=status.HTTP_200_OK)
    comment_id = request.POST.get('comment_id')
    value = request.POST.get('value')
    if abs(int(value)) != 1:
        return Response(
            {"warning": "اوه! یه مشکلی پیش اومده..."},
            status=status.HTTP_200_OK)
    try:
        com = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"warning": "همچین نظری وجود نداره!"},
            status=status.HTTP_200_OK)
    if CommentLike.objects.filter(user=request.user, comment=com):
        return Response(
            {"warning": "تو به این نظر، قبلا امتیاز دادی!"},
            status=status.HTTP_200_OK)
    CommentLike.objects.create(comment=com, user=request.user, value=value)
    return Response(
        {"message": "امتیازت ثبت شد! دستت درد نکنه..."},
        status=status.HTTP_200_OK)


@api_view(['GET'])
def del_avatar(request):
    if not request.user.is_authenticated:
        return Response(
            {"warning": "تو اصلا لاگین نکردی که میخوای عکس پروفایلت رو پاک کنی! اصلا اکانت داری؟"},
            status=status.HTTP_200_OK)
    try:
        request.user.profile.avatar.delete()
        return Response(
            {"message": "عکس پروفایلت پاک شد!"},
            status=status.HTTP_200_OK)
    except:
        return Response(
            {"warning": "اوه! یه مشکلی پیش اومده..."},
            status=status.HTTP_200_OK)


class TicketList(generics.ListAPIView):
    serializer_class = TicketListSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('topic', 'chats__code', 'chats__message')

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by('-create_datetime')


@api_view(['POST'])
@login_required
def send_ticket(request):
    code = request.POST.get('code')
    code = '' if code == '\u200b' else code
    chat = request.POST.get('chat')
    ticket_id = request.POST.get('ticket_id')
    topic = request.POST.get('topic')
    if chat:
        try:
            if ticket_id:
                tk = Ticket.objects.get(id=ticket_id)
            else:
                tk = Ticket(user=request.user, topic=topic)
                tk.save()
            tk.chats.create(user=request.user, code=code, message=chat)
            return Response(
                {
                    "ticket_id": tk.id,
                    "redirect_to": tk.get_absolute_url(),
                    "message": "تیکت شما برای من ارسال شد. سعی میکنم به زودی ببینم و پاسخ بدم!!<br> از طرف محمدرضا :)"
                },
                status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(
                {"warning": "اوه! یه مشکلی پیش اومده..."},
                status=status.HTTP_200_OK)
    else:
        return Response(
            {"warning": "فکر کنم یادت رفته مشکلت رو بنویسی!"},
            status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def toggle_status_ticket(request):
    ticket_id = request.POST.get('ticket_id')
    if ticket_id:
        try:
            tk = Ticket.objects.get(id=ticket_id)
            tk.closed = not tk.closed
            msg = "این تیکت بسته شد!<br>امیدوارم مشکلت حل شده باشه..." if tk.closed else 'تیکت تو دوباره باز شد!'
            tk.save()
            return Response(
                {
                    'closed': tk.closed,
                    "message": msg
                },
                status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(
                {"warning": "اوه! یه مشکلی پیش اومده..."},
                status=status.HTTP_200_OK)
    else:
        return Response(
            {"warning": "اوه! یه مشکلی پیش اومده..."},
            status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def send_ex_rate(request, ex_id):
    if not request.user.is_superuser:
        return Response(
            {"warning": "فقط خود محمدرضا میتونه به تمرین ها امتیاز بده!!"},
            status=status.HTTP_200_OK)
    student_id = request.POST.get('student')
    code = request.POST.get('code').replace('\u200b', '')
    try:
        student = User.objects.get(id=student_id)
        ex = CourseSessionExercise.objects.get(id=ex_id)
        ExerciseByStudent.objects.filter(user=student, exercise=ex).delete()
        ExerciseByStudent.objects.create(user=student, exercise=ex, code=code)
        return Response(
            {"message": "تمرین با موفقیت انجام شد!"},
            status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message": "این کاربر وجود ندارد!"},
            status=status.HTTP_200_OK)
    except CourseSessionExercise.DoesNotExist:
        return Response(
            {"message": "این تمرین وجود ندارد!"},
            status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def send_reply(request):
    code = request.POST.get('code').replace('\u200b', '')
    chat = request.POST.get('chat')
    ex_id = request.POST.get('ex_id')
    if chat:
        try:
            ex = CourseSessionExercise.objects.get(id=ex_id)
            chat_group, created = ex.chats.get_or_create(user=request.user)
            chat = chat_group.chat_set.create(code=code, message=chat)
            chat_group.save()
            return Response(
                {"message": "تیکت شما برای من ارسال شد. سعی میکنم به زودی ببینم و پاسخ بدم!!<br> از طرف محمدرضا :)"},
                status=status.HTTP_200_OK)
        except CourseSessionExercise.DoesNotExist:
            return Response(
                {"warning": "اوه! یه مشکلی پیش اومده..."},
                status=status.HTTP_200_OK)
    else:
        return Response(
            {"warning": "فکر کنم یادت رفته مشکلت رو بنویسی!"},
            status=status.HTTP_200_OK)
