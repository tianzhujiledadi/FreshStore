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
#在主urls.py里配置API接口逻辑
from django.contrib import admin#contrib普通发布版contrib普通发布版contrib普通发布版
from django.urls import path,include,re_path#include用于连接子路由，re_path用于正则
from Buyer.views import index
from rest_framework import routers#从API接口包导入路由器
from DjangoFresh.view import *
from CeleryTask.views import *
#从主模块视图导入类型类和用户类。
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     """声明数据"""
# c    class Meta:#元类
#         model=Goods#要进行接口序列化的模型
#         fields=["goods_name","goods_price","goods_number","goods_description"]#序列要返回的字段
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Goods.objects.all()#具体返回的数据
#     serializer_class = UserSerializer#指定过滤的类
# class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = GoodsType
#         fields = ["name","description"]
# class TypeViewSet(viewsets.ModelViewSet):
#     queryset = GoodsType.objects.all()
#     serializer_class = GoodsTypeSerializer
router = routers.DefaultRouter() #声明一个默认的路由注册器
router.register(r"goods",UserViewSet) #注册写好的接口视图，指向视图
router.register(r"goodsType",TypeViewSet) #注册写好的接口视图，指向视图
from  django.views.decorators.cache import cache_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include('Store.urls')),
    path('buyer/',include('Buyer.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    re_path(r'^$', index),
    path('get_add',get_add),
    #path('swv',cache_page(60*15)(small_white_views)),
    path('swv',small_white_views),
    #ckeditor类似于一个小APP
]
urlpatterns +=[
    re_path('^API', include(router.urls)),  # restful的根路由，指向router路由
    re_path("^api_auth", include("rest_framework.urls")),
    # 接口认证的根路由，指向rest_framework#API接口模块包路由
    path('test',test),
]


