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
from app_accounts import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('موارد-ذخیره-شده/', views.booked_items, name='booked-items'),
    path('ویرایش-پروفایل/', views.edit_profile, name='edit-profile'),
    path('مسائل-مطرح-شده-با-محمدرضا/', views.ticket_list, name='ticket-list'),
    path('طرح-مسئله-با-محمدرضا/', views.ticket_add, name='ticket-add'),
    path('مسائل-مطرح-شده-با-محمدرضا/<int:id>', views.ticket_detail, name='ticket-detail'),
    path('دوره-های-من', views.registered_items, name='registered-items'),
    path('resume/<str:username>/', views.resume, name='resume'),
    path('last-ex/', views.last_ex, name='last-ex'),
    path('last-tickets/', views.last_tickets, name='last-tickets'),
]