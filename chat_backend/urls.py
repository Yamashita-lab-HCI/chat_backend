"""chat_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

api_urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('check_username/', views.check_username, name='check_username'),
    path('messages/', views.message_view, name='messages'),
    path('check_login_status/', views.check_login_status, name='check_login_status'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(api_urlpatterns)),
    path('list-static/', views.list_static_files, name='list_static'),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='home'),
]

'''
if settings.DEBUG:
    urlpatterns += static('/static/' + settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''