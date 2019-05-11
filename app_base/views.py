from django.http import HttpResponse
from django.shortcuts import redirect
import os
import json
from app_base.templatetags.custom_tags import calc_price
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app_chat.models import Chat
from django.contrib import messages
from app_base.models import Course, CourseSession, ExerciseByStudent
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings


def protected_serve(request, path, document_root=None, show_indexes=False):
    if 'session/private-videos' not in path:
        return serve(request, path, document_root, show_indexes)
    else:
        item_id = path.split('/')[2]
        validate_cources = Course.objects.filter(id=item_id).first() in request.user.profile.registered_courses()
        validate_session = CourseSession.objects.filter(id=item_id).first() in request.user.profile.registered_sessions()
        if request.user.is_authenticated and (validate_session or validate_cources):
            return serve(request, path, document_root, show_indexes)
        else:
            return serve(request, settings.STATIC_URL + 'video/buy.mp4', '', show_indexes)


def home(request):
    ctx = {}
    ctx['courses'] = Course.objects.all()
    return render(request, 'home.html', ctx)


def course_detail(request, slug):
    ctx = {}
    ctx['course'] = course = Course.objects.get(slug=slug)
    ctx['courses'] = Course.objects.all().exclude(slug=slug)
    return render(request, 'course-detail.html', ctx)


def course_session_detail(request, course_slug, session_slug):
    ctx = {}
    course = Course.objects.get(slug=course_slug)
    ctx['session'] = course.coursesession_set.get(slug=session_slug)
    return render(request, 'course-session-detail.html', ctx)


def course_session_exercise_detail(request, course_slug, session_slug, exercise_slug):
    ctx = {}
    course = Course.objects.get(slug=course_slug)
    session = course.coursesession_set.get(slug=session_slug)
    ctx['exercise'] = ex = session.coursesessionexercise_set.get(slug=exercise_slug)
    ctx['chats'] = chats = ex.chats.filter(user=request.user)
    if chats.first():
        student = chats.first().user
        ctx['submited_final_reply'] = ExerciseByStudent.objects.filter(user=student, exercise=ex).last()
    return render(request, 'exercise-detail.html', ctx)


from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser)
def course_session_exercise_detail_with_reply(request, course_slug, session_slug, exercise_slug, student_id):
    ctx = {}
    course = Course.objects.get(slug=course_slug)
    session = course.coursesession_set.get(slug=session_slug)
    ctx['exercise'] = ex = session.coursesessionexercise_set.get(slug=exercise_slug)
    ctx['chats'] = chats = ex.chats.filter(user__id=student_id)
    if chats.first():
        student = chats.first().user
        ctx['submited_final_reply'] = ExerciseByStudent.objects.filter(user=student, exercise=ex).last()
    return render(request, 'exercise-detail.html', ctx)


@login_required
def register_course(request, item_id, item_type):
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    description = request.GET.get('description')
    if item_type not in ['Course', 'CourseSession']:
        messages.error(request, 'اوه! یه مشکلی پیش اومده...')
        return HttpResponseRedirect('/')
    model = eval(item_type)
    item = model.objects.get(id=item_id)
    if item_type == 'Course' and item not in [rc.course for rc in request.user.registereditem_set.all()]:
        if item.price:
            payment(request, item_id, item_type, phone, email, description)
        request.user.registereditem_set.create(course=item)
        for session in item.coursesession_set.all():
            request.user.registereditem_set.create(session=session)
        messages.success(
            request, '%s عزیز، خوشحالم که در این دوره شرکت کردی. حالا میتونی این دوره رو از توی پروفایلت با من شروع کنی :)' % request.user.username)
    elif item_type == 'CourseSession' and item not in [rs.session for rs in request.user.registereditem_set.all()]:
        if item.price:
            payment(request, item_id, item_type, phone, email, description)
        request.user.registereditem_set.create(session=item)
        aaa = [se for se in request.user.profile.registered_sessions() if se.course == item.course]
        if len(aaa) == item.course.coursesession_set.all().count():
            request.user.registereditem_set.create(course=item.course)
        messages.success(
            request, '%s عزیز، خوشحالم که در این قسمت رو گرفتی. حالا میتونی این قسمت رو از توی پروفایلت با من ادامه بدی کنی :)' % request.user.username)
    else:
        messages.success(
            request, '%s عزیز، شما قبلا در این دوره ثبت نام کرده اید!' % request.user.username)
    return HttpResponseRedirect(reverse('app-accounts:registered-items'))


@login_required
def change_seen_status(request):
    msg_id = request.GET.get('msg_id')
    if msg_id:
        try:
            msg_id = int(msg_id)
            msg = Chat.objects.filter(id=msg_id)
            if msg:
                msg_owner_groups = [gp.name for gp in msg[0].group.user.groups.all()]
                requested_user_groups = [gp.name for gp in request.user.groups.all()]
                if ('students' in msg_owner_groups and 'operators' in requested_user_groups) or \
                        ('operators' in msg_owner_groups and 'students' in requested_user_groups):
                    msg = msg[0]
                    msg.seen = True
                    msg.save()
        except ValueError:
            return HttpResponseBadRequest()
    response_data = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def payment(request, item_id, item_type, phone='09377000000', email='mail@example.com', description='خرید از پای‌تیچر'):
    """ price per toman """
    phone = request.GET.get('phone') if phone else phone
    email = request.GET.get('email') if email else email
    description = request.GET.get('description') if description else description
    ctx = {}
    if item_type not in ['Course', 'CourseSession']:
        messages.error(request, 'اوه! یه مشکلی پیش اومده...')
        return HttpResponseRedirect('/')
    if item_type == 'Course':
        item = Course.objects.get(id=item_id)
        price = calc_price(item, request.user)
    elif item_type == 'CourseSession':
        item = CourseSession.objects.get(id=item_id)
        price = item.price
    # Important: need to edit for realy server.
    CallbackURL = 'http://127.0.0.1:8000' + reverse('app-base:verify', args=(item_id, item_type))
    result = settings.CLIENT.service.PaymentRequest(settings.MERCHANT, price, description, email, phone, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    elif result.Status == 101:
        ctx['msg'] = 'این پرداخت قبلا با موفقیت انجام شده است. کد خطا: ' + str(result.Status)
    elif result.Status == -1:
        ctx['msg'] = 'اطلاعات ارسال شده ناقص است. کد خطا: ' + str(result.Status)
    elif result.Status == -2:
        ctx['msg'] = 'IP یا مرچنت کد پذیرنده صحیح نیست! کد خطا: ' + str(result.Status)
    elif result.Status == -3:
        ctx['msg'] = 'با توجه به محدودیت های شاپرک، امکان پرداخت با رقم درخواست داده شده میسر نیست! کد خطا: ' + \
            str(result.Status)
    elif result.Status == -4:
        ctx['msg'] = 'سطح تائید پذیرنده پایین تر از سطح نقره ای است! کد خطا: ' + str(result.Status)
    elif result.Status == -11:
        ctx['msg'] = 'درخواست مورد نظر یافت نشد! کد خطا: ' + str(result.Status)
    elif result.Status == -12:
        ctx['msg'] = 'امکان ویرایش درخواست میسر نیست! کد خطا: ' + str(result.Status)
    elif result.Status == -21:
        ctx['msg'] = 'هیچ نوع عملیات بانکی برای این تراکنش یافت نشد. کد خطا: ' + str(result.Status)
    elif result.Status == -22:
        ctx['msg'] = 'تراکنش نا موفق! کد خطا: ' + str(result.Status)
    elif result.Status == -33:
        ctx['msg'] = 'رقم تراکنش با رقم پرداخت شده مطابقت ندارد! کد خطا: ' + str(result.Status)
    elif result.Status == -34:
        ctx['msg'] = 'سقف تقسیم تراکنش از لحاظ تعداد یا رقم عبور نموده است! کد خطا: ' + str(result.Status)
    elif result.Status == -40:
        ctx['msg'] = 'اجازه دسترسی به متد مربوطه مجود ندارد! کد خطا: ' + str(result.Status)
    elif result.Status == -41:
        ctx['msg'] = 'اطلاعات ارسال شده به AdditionalData غیر معتبر است! کد خطا: ' + str(result.Status)
    elif result.Status == -42:
        ctx['msg'] = 'مدت زمان معتبر طول عمر شناسه پرداخت بین ۳۰ دقیقه تا ۴۵ روز است! کد خطا: ' + str(result.Status)
    elif result.Status == -54:
        ctx['msg'] = 'درخواست مورد نظر آرشیو شده است. کد خطا: ' + str(result.Status)
    else:
        ctx['msg'] = 'اوه! یه مشکلی پیش اومده. ظاهرا تراکنش ناموفق بوده یا توسط شما لغو شده است. کد خطا: ' + \
            str(result.Status)
    return render(request, 'verify-payment.html', ctx)


def verify(request, item_id, item_type):
    ctx = {}
    if item_type == 'Course':
        ctx['item'] = item = Course.objects.get(id=item_id)
        price = calc_price(item, request.user)
    elif item_type == 'CourseSession':
        ctx['item'] = item = CourseSession.objects.get(id=item_id)
        price = item.price
    if request.GET.get('Status') == 'OK':
        if item_type == 'Course':
            result = settings.CLIENT.service.PaymentVerification(settings.MERCHANT, request.GET['Authority'], price)
        elif item_type == 'CourseSession':
            result = settings.CLIENT.service.PaymentVerification(settings.MERCHANT, request.GET['Authority'], price)
        if result.Status == 100:
            ctx['status'] = 100
            ctx['msg'] = 'پرداخت با موفقیت انجام شد!'
            ctx['refid'] = result.RefID
            if item_type == 'Course':
                request.user.registereditem_set.create(course=item)
                for session in item.coursesession_set.all():
                    request.user.registereditem_set.create(session=session)
            elif item_type == 'CourseSession':
                request.user.registereditem_set.create(session=item)
                aaa = [se for se in request.user.profile.registered_sessions() if se.course == item.course]
                if len(aaa) == item.course.coursesession_set.all().count():
                    request.user.registereditem_set.create(course=item.course)
        elif result.Status == 101:
            ctx['msg'] = 'این پرداخت قبلا با موفقیت انجام شده است. کد خطا: ' + str(result.Status)
        elif result.Status == -1:
            ctx['msg'] = 'اطلاعات ارسال شده ناقص است. کد خطا: ' + str(result.Status)
        elif result.Status == -2:
            ctx['msg'] = 'IP یا مرچنت کد پذیرنده صحیح نیست! کد خطا: ' + str(result.Status)
        elif result.Status == -3:
            ctx['msg'] = 'با توجه به محدودیت های شاپرک، امکان پرداخت با رقم درخواست داده شده میسر نیست! کد خطا: ' + \
                str(result.Status)
        elif result.Status == -4:
            ctx['msg'] = 'سطح تائید پذیرنده پایین تر از سطح نقره ای است! کد خطا: ' + str(result.Status)
        elif result.Status == -11:
            ctx['msg'] = 'درخواست مورد نظر یافت نشد! کد خطا: ' + str(result.Status)
        elif result.Status == -12:
            ctx['msg'] = 'امکان ویرایش درخواست میسر نیست! کد خطا: ' + str(result.Status)
        elif result.Status == -21:
            ctx['msg'] = 'هیچ نوع عملیات بانکی برای این تراکنش یافت نشد. کد خطا: ' + str(result.Status)
        elif result.Status == -22:
            ctx['msg'] = 'تراکنش نا موفق! کد خطا: ' + str(result.Status)
        elif result.Status == -33:
            ctx['msg'] = 'رقم تراکنش با رقم پرداخت شده مطابقت ندارد! کد خطا: ' + str(result.Status)
        elif result.Status == -34:
            ctx['msg'] = 'سقف تقسیم تراکنش از لحاظ تعداد یا رقم عبور نموده است! کد خطا: ' + str(result.Status)
        elif result.Status == -40:
            ctx['msg'] = 'اجازه دسترسی به متد مربوطه مجود ندارد! کد خطا: ' + str(result.Status)
        elif result.Status == -41:
            ctx['msg'] = 'اطلاعات ارسال شده به AdditionalData غیر معتبر است! کد خطا: ' + str(result.Status)
        elif result.Status == -42:
            ctx['msg'] = 'مدت زمان معتبر طول عمر شناسه پرداخت بین ۳۰ دقیقه تا ۴۵ روز است! کد خطا: ' + str(result.Status)
        elif result.Status == -54:
            ctx['msg'] = 'درخواست مورد نظر آرشیو شده است. کد خطا: ' + str(result.Status)
        else:
            ctx['msg'] = 'پرداخت ناموفق! کد خطا: ' + str(result.Status)
    else:
        ctx['msg'] = 'اوه! یه مشکلی پیش اومده. ظاهرا تراکنش ناموفق بوده یا توسط شما لغو شده است.'
    return render(request, 'verify-payment.html', ctx)
