from __future__  import  absolute_import
from DjangoFresh.celery import app
import json
import requests
#在安装成功celery框架之后，django新生成的模块
@app.task#将taskExample转化为一个任务
def  taskExample():
    print('send email ok!')
    return '发送邮件成功'
@app.task
def add(x=1,y=2):
    return x+y
@app.task#装饰器
def DingTalk():
    url = "https://oapi.dingtalk.com/robot/send?access_token=bc824fcc163167495c020757343470c1ce4390f77c9dac0ce02fc3b3a8fb1590"
    print("函数调用成功")
    headers = {
        "Content-Type": "application/json",
        "Chartset":"utf-8"}
    requests_data={
        "msgtype":"text",
        "text": {
            "content": "天主极乐大帝祝你年薪百万"
        },
        "at":{
            "atMobiles":[],
        },
        "isAtAll":True
    }
    sendData=json.dumps(requests_data)
    response=requests.post(url,headers=headers,data=sendData)
    content=response.json()
    print(content)
    

