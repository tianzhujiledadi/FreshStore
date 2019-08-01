from rest_framework import viewsets
from DjangoFresh.serializers import *
from django_filters.rest_framework  import DjangoFilterBackend#导入过滤器
from  django.shortcuts import render
#当前部分还是为了自习接口的查询逻辑
class UserViewSet(viewsets.ModelViewSet):
    """
    查询所有的商品，并且实现了分页
    """
    queryset = Goods.objects.all()#具体返回的数据
    serializer_class = UserSerializer#指定过滤的类
    filter_backends = [DjangoFilterBackend]#选择采用哪个过滤器
    filterset_fields=["goods_name","goods_price"]#进行查询的字段
class TypeViewSet(viewsets.ModelViewSet):
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer
def text_api(request):
    return render(request,"store/test_api.html",locals())
