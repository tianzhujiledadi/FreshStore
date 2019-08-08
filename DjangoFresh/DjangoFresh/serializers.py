from rest_framework import serializers#从API接口包导入序列化器
#serializers序列化就是将一个列表变成一个生成器
from Store.models import *#从商城后台数据库模型包导入所有类
class  UserSerializer(serializers.HyperlinkedModelSerializer):
    #Hyperlinked超链接；Model模型；Serializer序列化器
    """声明数据"""
    class Meta:#元类；元类本身能够创建实例
        module=Goods#要进行接口序列化的模型
        fields=["goods_name","goods_price","goods_number","goods_description",
                "goods_date","goods_safeDafe"]#序列要返回的字段

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsType
        fields = ["name","description"]

# 此对象( 类) 本身是能够创建( 实例) ， 这就是为什么它是一个类的对象 . [1]
# 因此
# 你可以将它赋给一个变量
# 你可以复制它
# 你可以向它添加属性
# 你可以将它作为函数的参数 [2]
# 元类
# 1
# 2
# 3
# MyClass = MetaClass()
# MyObject = MyClass()
# MyClass = type('MyClass', (), {})
# 函数 type实际上就是一个元类，在Python中，包括int ，str ，函数和类，所有的都是对象。
