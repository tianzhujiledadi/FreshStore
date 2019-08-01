from  rest_framework.renderers import JSONRenderer
class  customrenderer(JSONRenderer):
    def render(self,data,accepted_media_type=None,renderer_context=None):
        """
        :param data: 返回的数据
        :param accepted_media_type: 接收的类型
        :param renderer_context: 呈现的内容
        :return:
        """
        if renderer_context:#if request.method=="POST"如果有请求的数据过来#
            if isinstance(data,dict):#判断返回的类型是否是字典
                msg=data.pop("msg","请求成功")#如果是字典获取字典当中的msg参数
                code=data.pop("code",0)#如果是字典获取字典当中的code参数
            else:#非字典类型
                msg="请求成功"
                code=0
            ret={
                "msg":msg,
                "code":code,
                "author":"李易松超帅",
                "data":data
            }#重新构建返回数据格式
            return super().render(ret,accepted_media_type,renderer_context)#返回数据格式
        else:
            return super().render(data,accepted_media_type,renderer_context)
            #如果没有发生修改，返回原格式
from rest_framework.renderers import JSONRenderer
#rest_framework接口测试包，renderers类，JSONRenderer方法
class customrenderer(JSONRenderer):
    def render(self,data,accepted_media_type=None,renderer_context=None):#默认为空
        """

        :param data:返回的数据
        :param accepted_media_type:接收的类型
        :param renderer_context:呈现的内容
        :return:
        """
        if renderer_context:#if  request.method=="POST"#如果有请求的数据过来
            if isinstance(data,dict):#判断返回的数据是否是字典
                msg=data.pop("msg","请求成功")#如果是字典获取字典当中的msg参数
                code=data.pop("code",0)#如果是字典获取字典当中的code参数
            else:#非字典类型
                msg="请求成功"
                code=0
            ret={
                "msg":msg,
                "code":code,
                "author":"把",
                "data":data
            }#重新构建返回数据格式
            return super().render(ret,accepted_media_type,renderer_context)

