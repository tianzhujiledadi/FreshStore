"""DjangoFresh URL Configuration

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
from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("index/",index),
    path("base/",base),
    path("register_store/",register_store),
    path("add_goods/",add_goods),
    re_path(r"list_goods/(?P<state>\w+)/",list_goods),
    path("loginout/",loginout),
    re_path(r'^goods/(?P<goods_id>\d+)',goods),
    re_path(r'update_goods/(?P<goods_id>\d+)',update_goods),
    re_path(r"set_goods/(?P<state>\w+)/",set_goods),
    re_path(r"setgoodstype/(?P<state>\w+)/",setGoodType),
    path("goodstype/",goodstype),
# path("addgoodtype/",addGoodType),
]
