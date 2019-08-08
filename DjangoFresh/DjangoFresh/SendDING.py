#coding:utf-8
import json#导入json模块
import requests#导入请求模块
def DingTalk():
    url = "https://oapi.dingtalk.com/robot/send?access_token=bc824fcc163167495c020757343470c1ce4390f77c9dac0ce02fc3b3a8fb1590"
    headers = {
        "Content-Type": "application/json",
        "Chartset":"utf-8"
    }
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

DingTalk()

