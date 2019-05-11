from django.shortcuts import render
from app_accounts.models import RegisteredItem
from app_social.models import Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_accounts.forms import ProfileForm
from app_accounts.models import Profile
from app_chat.models import Ticket
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.forms.models import modelform_factory
from app_base.models import CourseSessionExercise
from app_chat.models import ChatGroup
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def profile(request):
    ctx = {}
    ctx['registered_course'] = [rc.course for rc in request.user.registereditem_set.all()]
    return render(request, 'student-dashboard.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def last_ex(request):
    ctx = {}
    page_num = request.GET.get('page') if request.GET.get('page') else 1
    ct = ContentType.objects.get_for_model(CourseSessionExercise.objects.first())
    student = request.GET.get('student')
    if student:
        all_chats = ChatGroup.objects.filter(
            user__username=student, content_type=ct).distinct(
            'content_type', 'object_id', 'user').order_by('-object_id').chat_set.all()
    else:
        all_chat_groups = ChatGroup.objects.filter(
            user__groups__name='students', content_type=ct).distinct(
            'content_type', 'object_id', 'user')
        all_chats = []
        for g in all_chat_groups:
            for chat in g.chat_set.all().distinct('seen').order_by('seen'):
                all_chats.append(chat)
    for chat in all_chats:
        chat.abs_url = chat.group.content_object.get_absolute_student_reply_url(chat.group.user.id)

    p = Paginator(all_chats, 20)
    ctx['page_num'] = page_num
    ctx['num_pages'] = p.num_pages
    ctx['page'] = p.page(page_num)
    return render(request, 'last-ex.html', ctx)



@user_passes_test(lambda u: u.is_superuser)
def last_tickets(request):
    ctx = {}
    page_num = request.GET.get('page') if request.GET.get('page') else 1
    all_tickets = Ticket.objects.all().order_by('-create_datetime')
    p = Paginator(all_tickets, 20)
    ctx['page_num'] = page_num
    ctx['num_pages'] = p.num_pages
    ctx['page'] = p.page(page_num)
    return render(request, 'last-tickets.html', ctx)


def resume(request, username):
    try:
        user = User.objects.get(username=username)
        if user.profile.show_resume:
            return render(request, 'resume.html', {'user': user})
    except User.DoesNotExist:
        messages.error(request, 'اوه! یه مشکلی پیش اومده...')
    return redirect(reverse('app-base:home'))


@login_required
def booked_items(request):
    ctx = {}
    booked_items = Bookmark.objects.filter(user=request.user)
    ctx['items'] = [book_item.content_object for book_item in booked_items]
    return render(request, 'booked-items.html', ctx)


@login_required
def edit_profile(request):
    ctx = {}
    if request.method == 'POST':
        ctx['form'] = form = ProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            ctx['form'] = form
    else:
        ctx['form'] = form = ProfileForm(user=request.user)
    ctx['new_avatar'] = Profile.objects.get(user=request.user).avatar
    return render(request, 'student-profile.html', ctx)


@login_required
def ticket_list(request):
    ctx = {}
    page_num = request.GET.get('page') if request.GET.get('page') else 1
    ctx['tickets'] = tickets = Ticket.objects.filter(user=request.user).order_by('-id')
    p = Paginator(tickets, 10)
    ctx['page_num'] = page_num
    ctx['num_pages'] = p.num_pages
    ctx['page'] = p.page(page_num)
    return render(request, 'ticket-list.html', ctx)


@login_required
def ticket_add(request):
    return render(request, 'ticket-add.html')


@login_required
def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.user.is_superuser or ticket.user == request.user:
        return render(request, 'ticket-detail.html', {'ticket': ticket})
    else:
        return redirect(reverse('app-accounts:profile'))


@login_required
def registered_items(request):
    ctx = {}
    registered_items = request.user.registereditem_set.all().order_by('-id')
    ctx['registered_items'] = set([i.session.course for i in registered_items if i.session])
    return render(request, 'registered-items.html', ctx)
