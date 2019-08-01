# import  requests#互亿
# url="http://106.ihuyi.com/webservice/sms.php?method=Submit"#请求地址
# account="C08900956"#验证码通知短信APIID
# password="f85bfe96509034a6dd3c4fb983c0494f"#密码APIKEY
# mobile="18833005997"#被发送手机号
# content="	您的验证码是：666666。请不要把验证码泄露给其他人。"
# #定义请求的头部
# headers={
#     "Content-type":"application/x-www-form-urlencoded",
#     "Accept":"text/plain"
# }
# #定义请求的数据
# data={
#     "account":account,
#     "password":password,
#     "mobile":mobile,
#     "content":content,
# }
# #发起数据
# response=requests.post(url,headers=headers,data=data)
# #url请求的地址
# #headers请求的头部
# #data请求的数据
# print(response.content.decode())#输出密码发送结果
#################################################################################################################################################
#云之讯短信
# import json
# import requests
# url = "https://open.ucpaas.com/ol/sms/sendsms"
# sid = ""
# token = ""
# appid = ""
# templateid = ""
# param = "0506"
# mobile = ""
# headers = {
#     'Accept': 'application/json',
#     'Content-Type': 'application/json;charset=utf-8'
# }
# #定义请求的数据
# data = {
#     "sid": sid,
#     "token": token,
#     "appid": appid,
#     "templateid": templateid,
#     "param": param,
#     "mobile": mobile,
# }
# #发起数据
# response = requests.post(url,headers = headers,data=json.dumps(data))
#     #url 请求的地址
#     #headers 请求头部
#     #data 请求的数据
# print(response.json())
import requests#互亿
url="http://106.ihuyi.com/webservice/sms.php?method=Submit"#请求地址；互亿固定
account="C08900956"#验证码通知短信APIID
password='f85bfe96509034a6dd3c4fb983c0494f'#密码APIKEY
mobile="18833005997"#被发送手机号
content="	您的验证码是：666663。请不要把验证码泄露给其他人。"
#定义请求的头部
headers={
    "Content-type":"application/x-www-form-urlencoded",
    "Accept":"text/plain"
}
#定义请求的数据
data={
    "account":account,
    'password':password,
    "mobile":mobile,
    "content":content,
}
#发起数据
response=requests.post(url,headers=headers,data=data)
#url请求的地址
#headers请求的地址
#data请求的数据
print(response.content.decode())#decode将数据解码




