"""
URL configuration for my_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from controller import SystemController as Sc
from controller import Robot as Rc

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Sc.go_index),
    path("login/", Sc.login_page),  # 登录页面
    path("api/get_conversations/", Rc.get_conversations),
    path("api/get_messages/", Rc.get_messages),
    path("api/send_message/", Rc.send_message),
    path("api/create_conversation/", Rc.create_conversation),
    path("api/register/", Rc.register),
    path("api/login/", Rc.login),
    path('api/delete_user/', Rc.delete_user),  # 新增注销接口
    path('api/delete_conversation/', Rc.delete_conversation),  # 新增删除会话接口
]
