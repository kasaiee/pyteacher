"""pyteacher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app_base import views
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('change-seen-status/', views.change_seen_status, name='change-seen-status'),

    path('course-detail/<str:slug>/', views.course_detail, name='course-detail'),
    path('register-course/<int:item_id>-<str:item_type>/', views.register_course, name='register-course'),
    path('payment/<int:item_id>-<str:item_type>/', views.payment, name='payment'),
    path('verify/<int:item_id>-<str:item_type>/', views.verify, name='verify'),
    path('<str:course_slug>/<str:session_slug>/', views.course_session_detail, name='course-session-detail'),
    path('<str:course_slug>/<str:session_slug>/<str:exercise_slug>/',
         views.course_session_exercise_detail, name='course-session-exercise-detail'),
    path('<str:course_slug>/<str:session_slug>/<str:exercise_slug>/<int:student_id>',
         views.course_session_exercise_detail_with_reply, name='course-session-exercise-detail-with-reply'),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], views.protected_serve, {
        'document_root': settings.MEDIA_ROOT})
]
