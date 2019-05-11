from django import template
from app_base.models import ExerciseByStudent

register = template.Library()


@register.filter
def get_type(obj):
    return obj.__class__.__name__


@register.filter
def your_investment(item, user):
    if user.is_authenticated:
        return sum([ri.session.price for ri in user.registereditem_set.filter(session__course=item)])
    else:
        return 0


@register.filter
def calc_price(item, user):
    if user.is_authenticated:
        return item.price() - your_investment(item, user)
    else:
        return item.price()


@register.filter
def is_bought_session(session, user):
    if not user.is_authenticated:
        return False
    elif session.price == 0:
        return True
    else:
        return session in user.profile.registered_items()


@register.filter
def get_user_ex_rate(ex, user):
    if not user.is_authenticated:
        return 0
    try:
        return ExerciseByStudent.objects.get(user=user, exercise=ex).rate
    except ExerciseByStudent.DoesNotExist:
        return 0


def gen_color():
    while True:
        yield 'teal'
        yield 'orange'
        yield 'blue'
        yield 'green'
        yield 'pink'
        yield 'yellow'
        yield 'red'


color_gen = gen_color()


@register.filter
def get_color(temp):
    return next(color_gen)


@register.filter
def is_done(ex, user):
    if user.is_anonymous:
        return False
    elif ExerciseByStudent.objects.filter(exercise=ex, user=user):
        return True
    return False
