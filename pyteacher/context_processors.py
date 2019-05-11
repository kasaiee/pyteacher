from django.conf import settings


def get_settings_value(request):
    return {
        'DEFAULT_USER_AVATAR': settings.DEFAULT_USER_AVATAR
    }
