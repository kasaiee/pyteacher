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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include(('app_api.urls', 'app_api'), namespace='app-api')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    path('profile/', include(('app_accounts.urls', 'app_accounts'), namespace='app-accounts')),
    path('', include(('app_base.urls', 'app_base'), namespace='app-base')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
