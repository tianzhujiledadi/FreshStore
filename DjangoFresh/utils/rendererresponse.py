
from rest_framework.renderers import JSONRenderer
#重写API接口包；rest_framework接口模块； renderers渲染器
#rest_framework接口模块下的渲染器包导入JSON渲染器类
class customrenderer(JSONRenderer):#custom定制custom customrenderer#定制渲染器
    def render(self,data,accepted_media_type=None,renderer_context=None):
#render实施；renderer渲染器；context内容；renderer_context#渲染器内容
#data数据；accepted接收；media媒介，媒体；type类型；
#accepted_media_type接收的媒体类型
        if renderer_context:#如果渲染内容不为空，即有数据传过来
            if isinstance(data,dict):#判断返回的数据是否是字典
                #instance实例；isinstance,判断类型
                msg=data.pop("msg","请求成功")#如果是字典获取字典当中的msg参数
                code=data.pop("code",0)#将字典中的数据取出来
            else:#非字典类型
                msg="请求成功"
                code:0#密码，编码，代码
            ret={
                "msg":msg,
                "code":code,
                "author":"李易松",
                "data":data
            }#重新构建返回数据格式
            return super().render(ret,accepted_media_type,renderer_context)#返回数据格式
        else:
            return super().render(data,accepted_media_type,renderer_context)
        #如果没有修改返回原格式。

