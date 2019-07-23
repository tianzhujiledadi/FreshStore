import hashlib
from django.shortcuts import render,HttpResponseRedirect
from  Store.models import *
def setpw(password):
    md5=hashlib.md5()#实例化hashlib包的md5类
    md5.update(password.encode())#对密码进行加密
    return  md5.hexdigest()#返回加密的值

def LoginValid(fun):
    def  inner(request):
        username=request.COOKIES.get("username")
        session_user=request.session.get("username")
        if username  and  session_user:
            user=   Seller.objects.filter(username=username).first()
            if  user  and username==session_user:
                return fun(request)
        return HttpResponseRedirect("/store/login/")
    return inner
@LoginValid #验证是否cookie和session是否正确
def  index(request):
    user_id=request.COOKIES.get("user_id")
    if  user_id:
        user_id=int(user_id)
    else:
        user_id=0#通过用户查询店铺是否存在（店铺和用户通过用户的id进行关联）
    store=Store.objects.filter(user_id=user_id).first()
    if store:
        is_store=1
    else:
        is_store=0
    return render(request,'store/index.html',{"is_store":is_store})
def  register(request):
    if request.method=="POST":
        username=request.POST.get("username")#POST请求类型 get得到
        password=request.POST.get("password")
        if  username and password:
            seller=Seller()
            seller.username=username
            seller.password=setpw(password)
            seller.save()
            return  HttpResponseRedirect("/store/login/")
    return render(request, 'store/register.html')#如果是get请求方式返回注册页面
def  login(request):
    response=render(request,"store/login.html")
    response.set_cookie("a", "b")
    if  request.method=="POST":
        username=request.POST.get("username")#POST请求类型get得到
        password=request.POST.get("password")
        if  username   and  password:
            user=userValid(username)
            if  user:
                web_password=setpw(password)
                cookies=request.COOKIES.get("a")
                if user.password == web_password and cookies == "b":
                    response = HttpResponseRedirect("/store/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id",user.id)
                    request.session["username"] = username
                    return response
    return response
# Create your views here.


def userValid(username):#检验用户名是否存在
    user=Seller.objects.filter(username=username).first()
    return user
def base(request):
    return render(request,'store/base.html')
def register_store(request):
    type_list=StoreType.objects.all()
    if request.method=="POST":
        post_data=request.POST#接收post数据
        store_name=post_data.get("store_name")
        store_descrition=post_data.get("store_descrition")
        store_phone=post_data.get("store_phone")
        store_money=post_data.get("store_money")
        store_address = post_data.get("store_address")
        user_id=int(request.COOKIES.get("user_id"))#通过cookie来得到user_id
        type_list=post_data.get("type")
        store_logo=request.FILES.get("store_logo")
        store=Store()
        store.store_name=store_name
        store.store_descrition = store_descrition
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.type_list = type_list
        store.store_logo = store_logo
        store.save()
        for i in type_list:
            store_type=StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
    return render(request,"store/register_store.html",locals())
