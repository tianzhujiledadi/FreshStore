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
    print(222222222)
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
def userValid(username):#检验用户名是否存在
    user=Seller.objects.filter(username=username).first()
    return user
def base(request):
    return render(request,'store/base.html')
def register_store(request):
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST #接收post数据
        store_name = post_data.get("store_name")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")
        user_id =int(request.COOKIES.get("user_id")) #通过cookie来得到user_id
        type_lists = post_data.getlist("type") #通过request.post得到类型，但是是一个列表
        #type_lists = post_data.get("type")  # 通过request.post得到类型，获取最后一个数据
        store_logo = request.FILES.get("store_logo") #通过request.FILES得到
        #保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo #django1.8之后图片可以直接保存
        store.save() #保存，生成了数据库当中的一条数据
        #在生成的数据当中添加多对多字段。
        for i in type_lists: #循环type列表，得到类型id
            #store_type = StoreType.objects.get(id = i) #查询类型数据，获取最后一个数据
            store_type=StoreType.objects.get(id=i)#获取多个数据封装到列表
            store.type.add(store_type) #添加到类型字段，多对多的映射表
        store.save() #保存数据
    return render(request,"store/register_store.html",locals())
def  add_goods(request):
    if request.method=="POST":
        post_data = request.POST  # 接收post数据
        goods_name = post_data.get("goods_name")
        goods_price = post_data.get("goods_price")
        goods_image=request.FILES.get("goods_image")
        goods_number = post_data.get("goods_number")
        goods_description = post_data.get("goods_description")
        goods_date = post_data.get("goods_date")  # 通过request.FILES得到
        goods_safeDate = post_data.get("goods_safeDate")
        goods_store = post_data.get("goods_store")
        # 保存非多对多数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()
        # 保存多对多数据
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
    return render(request, "store/add_goods.html")
from django.core.paginator import Paginator
def  list_goods(request):#分页并且查询
    """商品的列表页"""
    keywords=request.GET.get("keywords","")
    page_num=request.GET.get("page_num",1)
    if  keywords:
        goods_list = Goods.objects.filter(id__contains=keywords)  # goods_name只是一个字段名，contains包含
        #goods_list=Goods.objects.filter(goods_name__contains=keywords)
    else:
        goods_list=Goods.objects.all()
    paginator=Paginator(goods_list,3)#分页，每页3条数据
    page=paginator.page(int(page_num))
    page_range=paginator.page_range
    return  render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords,"goods_list":goods_list})
# def list_goods(request):#仅查询
#     keywords=request.GET.get("keywords","")
#     if  keywords:
#         goods_list=Goods.objects.filter(id__contains=keywords)#goods_name只是一个字段名，contains包含
#     else:
#         goods_list=Goods.objects.all()
#     page=goods_list
#     return render(request,"store/goods_list.html",locals())
# from  django.core.paginator import  Paginator#django开发的分页模块
# def  list_goods(request):#仅分页
#     page_num=request.GET.get("page_num",1)#默认是第一页
#     goods_list=Goods.objects.order_by("-id")#查询goods表中所有数据，并按倒序排序
#     paginator=Paginator(goods_list,3)#将获取的所有数据按每页3条数据分页
#     page=paginator.page(int(page_num))#获取具体页的数据
#     page_range=paginator.page_range#获取所有页码
#     return render(request,"store/goods_list.html",locals())
def  loginout(request):
    print(111111)
    response=HttpResponseRedirect("/store/login/")
    response.delete_cookie("username")
    response.delete_cookie("a")
    del request.session["username"]
    return  response
def  goods(request,goods_id):
    goods_data=Goods.objects.filter(id=goods_id).first()
    return  render(request,"store/goods.html",locals())
def  update_goods(request,goods_id):
    goods_data=Goods.objects.filter(id=goods_id).first()
    if request.method=="POST":
        post_data = request.POST  # 接收post数据
        goods_name = post_data.get("goods_name")
        goods_price = post_data.get("goods_price")
        goods_image = request.FILES.get("goods_image")
        goods_number = post_data.get("goods_number")
        goods_description = post_data.get("goods_description")
        goods_date = post_data.get("goods_date")  # 通过request.FILES得到
        goods_safeDate = post_data.get("goods_safeDate")
        # 保存非多对多数据
        goods = Goods.objects.get(id=int(goods_id))#根据id得到该条数据，get数据没有或有多条数据会报错
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/store/goods/%s"%goods_id)#重定向到对应id的商品详情页
    return  render(request,"store/update_goods.html",locals())












