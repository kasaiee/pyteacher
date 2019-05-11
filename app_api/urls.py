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
from app_api import views
from rest_framework.authtoken import views as auth_view


urlpatterns = [
    path('token/', auth_view.obtain_auth_token),
    path('like/', views.like, name='like'),
    path('bookmark/', views.bookmark, name='bookmark'),
    path('comment/', views.comment, name='comment'),
    path('comment-list/', views.comment_list, name='comment-list'),
    path('comment-like/', views.comment_like, name='comment-like'),
    path('del-avatar/', views.del_avatar, name='del-avatar'),
    path('send-ticket/', views.send_ticket, name='send-ticket'),
    path('send-reply/', views.send_reply, name='send-reply'),
    path('ticket-list/', views.TicketList.as_view(), name='ticket-list'),
    path('toggle-status-ticket/', views.toggle_status_ticket, name='toggle-status-ticket'),
    path('send-ex-rate/<str:ex_id>', views.send_ex_rate, name='send-ex-rate'),
]