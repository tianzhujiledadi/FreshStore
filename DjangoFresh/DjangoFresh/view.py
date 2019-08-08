from rest_framework import viewsets
from DjangoFresh.serializers import *#serializers序列化器serializers序列化器serializers
#从主模块的序列化器包导入所有类
from django_filters.rest_framework  import DjangoFilterBackend#导入过滤器#backend后端backend
from  django.shortcuts import render,HttpResponse#shortcuts捷径的复数
#当前部分还是为了自习接口的查询逻辑
class UserViewSet(viewsets.ModelViewSet):
    """
    查询所有的商品，并且实现了分页
    """
    queryset=Goods.objects.all()#返回商品表所有数据
    serializer_class=UserSerializer#指定实例化的类
    filter_backends=[DjangoFilterBackend]#选择采用哪个过滤器
    filterset_fields=["goods_name","goods_price"]#进行查询的字段

class TypeViewSet(viewsets.ModelViewSet):
    queryset = GoodsType.objects.all()#返回商品类型表所有数据
    serializer_class = GoodsTypeSerializer#指定实例化的类
def text_api(request):
    return render(request,"store/test_api.html",locals())

from  django.views.decorators.cache import cache_page
from django.core.cache import cache
# @cache_page(60*15)
# def small_white_views(request):
#     print("我是小白视图")
#     #raise TypeError("我就不想好好的")
#     return HttpResponse("我是小白视图")
def small_white_views(request):#底层缓存接口
    store_data=cache.get("store_data")#如果没有返回None
    if store_data:
        store_data=store_data
    else:
        data=Store.objects.all()
        cache.set("store_data",data,30)#30缓存周期#读取缓存页面
        #cache.add("store_data", data, 30)#add只会添加一个缓存，不会修改已有的缓存
        store_data=data
    return render(request,"store/test.html",locals())
def  small_white_views(request):#底层缓存接口
    store_data=cache.get("store_data")#如果没有返回None
    if  store_data:
        store_data=store_data
    else:
        data=Store.objects.all()
        cache.set("store_data",data,30)#缓存周期#读取缓存页面
        store_data=data
    return render (request,"store/test.html",locals())
#set设置cache;get获取cache;add添加cache

# def small_white_views(request):
#     rep=HttpResponse("i an rep")
#     rep.render=lambda:HttpResponse("hello world")
#     return rep
def test(request):
    print('页面粒度缓存')
    response = render(request,"store/test.html/",locals())
    response.set_cookie("valid", "123456")
    return response


