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
from Buyer.views import *
urlpatterns = [
    path('index/',index),
    path('base/',base),
    path('login/',login),
    path('register/',register),
    path('logout/',logout),
    re_path(r'goods_list/',goods_list),
    path('logout/',logout),
    path('pay_order/',pay_order),
    path('pay_result/',pay_result),
    path('detail/',detail),
    path('place_order/',place_order),#订单列表
    path('cart/',cart),
    path('add_cart/',add_cart),
    path('testgoods/',TestGoods),#批量添加商品
    path('goodsexit/',goodsexit),#批量修改商品
]

