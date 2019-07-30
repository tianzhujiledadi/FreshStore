import hashlib
from django.shortcuts import render,HttpResponseRedirect
from  Store.models import *
def setpw(password):
    md5=hashlib.md5()#实例化hashlib包的md5类
    md5.update(password.encode())#对密码进行加密
    return  md5.hexdigest()#返回加密的值
def LoginValid(fun):#被包装的函数名和参数都在fun里
    def  inner(request,*args,**kwargs):#*args,**kwargs,表示什么参数都能传，一般这样写，参数较少时可以灵活更改
        #request,是浏览器返回来的参数，*args将参数打包成元组，**kwargs将关键字参数打包成字典
        username=request.COOKIES.get("username")
        session_user=request.session.get("username")
        if username  and  session_user and username==session_user:
            user=Seller.objects.filter(username=username).first()#判断存在该用户
            if  user:
                return fun(request,*args,**kwargs)#调用下面被装饰的函数
        return  HttpResponseRedirect("/store/login/")
    return inner#继承fun里传过来的参数调用里面的函数
@LoginValid #验证是否cookie和session是否正确
def  index(request):#调用被包装的
    return render(request,'store/index.html',locals())
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

def login(request):
    response=render(request,"store/login.html")
    response.set_cookie("a",'b')
    if request.method=='POST':
        username=request.POST.get("username")#POST请求类型get得到
        password=request.POST.get("password")
        if  username  and  password:
            user=userValid(username)#检验用户是否存在
            if user:
                web_password=setpw(password)
                cookies=request.COOKIES.get('a')#检验密码是否来源登录页面
                if  user.password==web_password  and  cookies=="b":
                    response=HttpResponseRedirect("/store/index/")
                    response.set_cookie("username",username)
                    response.set_cookie("user_id",user.id)
                    request.session["username"]=username
                    store=Store.objects.filter(user_id=user.id).first()#在查询店铺是否存在
                    if store:
                        response.set_cookie('has_store',store.id)
                    else:
                        response.set_cookie('has_store','')
    return  response

def userValid(username):#检验用户名是否存在
    user=Seller.objects.filter(username=username).first()
    return user
def base(request):
    return render(request,'store/base.html')
def register_store(request):
    type_list = StoreType.objects.all()
    user_id=request.COOKIES.get("user_id")#获取用户id
    print(user_id,"user_id")
    if request.method == "POST":
        print(111111)
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
        response=HttpResponseRedirect('/store/store_list/')#在这里重定向店铺列表页
        response.set_cookie('has_store',store.id)
        return  response
    return render(request,"store/register_store.html",locals())
def  add_goods(request):
    goodstype_list = GoodsType.objects.all()
    if request.method=="POST":
        post_data = request.POST  # 接收post数据
        goods_name = post_data.get("goods_name")
        goods_price = post_data.get("goods_price")
        goods_image=request.FILES.get("goods_image")
        goods_number = post_data.get("goods_number")
        goods_description = post_data.get("goods_description")
        goods_date = post_data.get("goods_date")  # 通过request.FILES得到
        goods_safeDate = post_data.get("goods_safeDate")
        goods_type = post_data.get("type")#在前台获取的商品类型
        print(type(goods_type))
        goods_store = post_data.get("store_id")
        print(goods_store,6666666666666666666)
        #goods_store=request.COOKIES.get("has_store")#在后台过的店铺id

        # 保存非多对多数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.store_id = Store.objects.get(id=int(goods_store))
        #多对一#将goods_type赋值给GoodsType表的id
        goods.save()
        # 保存多对多数据
        print("保存成功")
        #return  HttpResponseRedirect('/store/list_goods/up/?store_id=%s'%goods_store)
        return HttpResponseRedirect('/store/list_goods/up/?store_id='+goods_store)
        #重定向商品列表，因为商品列表函数获取前端的店铺id所以不用被登录校验装饰
    store_id = request.GET.get("store_id")
    print(store_id,99999999999999999999)
    return render(request, "store/add_goods.html/",locals())
from django.core.paginator import Paginator
def  list_goods(request,state):#分页并且查询

    """商品的列表页"""
    if state=="down":
        state_num=0
    else:
        state_num = 1
    keywords=request.GET.get("keywords","")#查询关键词
    page_num=request.GET.get("page_num",1)#页码
    #查询店铺
    store_id = request.GET.get("store_id")
    print(store_id,"store_id")
    #store_id=request.COOKIES.get("has_store")#获取前端的has_store即id值
    print(store_id)
    store=Store.objects.get(id=int(store_id))#根据id获取对应店铺的对象
    if  keywords:
        #goods_list = Goods.objects.filter(id__contains=keywords)  # goods_name只是一个字段名，contains包含
        goods_list=store.goods_set.filter(goods_under=state_num,goods_name__contains=keywords)#完成了模糊查询
        #goods_list=Goods.objects.filter(goods_name__contains=keywords)
    else:#如果关键词不存在，查询所有该店铺商品
        #goods_list=Goods.objects.all()
        goods_list=store.goods_set.filter(goods_under=state_num)#store是获取的店铺，goods是商品表名，_set.all是固定语法
    paginator=Paginator(goods_list,3)#分页，每页3条数据
    page_num=int(page_num)
    if len(goods_list)/3<=page_num-1:
        if page_num>=2:
            page_num-=1
        else:
            page_num=1
    page = paginator.page(int(page_num))
    page_range=paginator.page_range
    return  render(request,"store/goods_list.html",locals())
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
    # response.delete_cookie("username")
    # response.delete_cookie("a")
    for  key  in request.COOKIES:#获取当前所有cookie
        response.delete_cookie(key)
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
def  set_goods(request,state):
    if  state=="down":
        state_num=0
    else:
        state_num = 1
    id=request.GET.get("id")#get获取id
    #referer=request.META.get('HTTP_REFERER')#返回当前请求的来源地址
    referer=request.META.get('HTTP_REFERER')#返回当前请求的来源地址
    if id:
        goods = Goods.objects.filter(id=id).first()
        if state=='delete':
            goods.delete()
        else:
            goods.goods_under=state_num#修改状态
            goods.save()#保存
    return HttpResponseRedirect(referer)#跳转到请求来源页
def  goodstype(request):
    page_num=request.GET.get("page_num",1)#默认是第一页
    goodstype_list=GoodsType.objects.order_by("id")#查询goods表中所有数据，并按倒序排序
    paginator=Paginator(goodstype_list,3)#将获取的所有数据按每页3条数据分页
    page_num = int(page_num)
    print(len(goodstype_list),1)
    print(page_num - 1,2)
    if len(goodstype_list) / 3 <= page_num - 1:
        if page_num >= 2:
            page_num -= 1
        else:
            page_num = 1
    print(page_num,3)
    page = paginator.page(int(page_num))
    page_range=paginator.page_range#获取所有页码
    return render(request,"store/goodstype.html",locals())
def setGoodType(request,state):
    if state=="add"  or state=="exit":
        post_data = request.POST  # 接收post数据
        name = post_data.get("name")
        description = post_data.get("description")
        picture = request.FILES.get("picture")
        if state=="add":
            goodstype=GoodsType()
        else:
            id = request.POST.get("id")  # get获取id
            print(id,6)
            goodstype=GoodsType.objects.filter(id=id).first()
        goodstype.name=name
        goodstype.description=description
        goodstype.picture=picture
        goodstype.save()
    elif state=="del":
        id=request.GET.get("id")
        goodstype = GoodsType.objects.filter(id=id).first()
        goodstype.delete()
    else:
        pass
    referer = request.META.get('HTTP_REFERER')#获取请求页来源
    return HttpResponseRedirect(referer)#跳转到请求来源页
from  Buyer.models import OrderDetail,Order
def order_list(request):#订单
    status=request.GET.get("status")
    store_id=request.COOKIES.get("has_store")#通过cookie获取店铺id
    order_list=OrderDetail.objects.filter(order_id__order_status=int(status),goods_store=store_id)
    #获取商品对应的店铺id,获取订单对应的状态
    return render(request,"store/order_list.html",locals())
def orderdeal(request):#订单处理
    id=request.GET.get("id")
    status=request.GET.get("status")
    order = Order.objects.get(id=int(id))
    order.order_status=status
    order.save()

    return  HttpResponseRedirect("/store/order_list/?status="+status)
def store_list(request):#店铺列表
    keywords = request.GET.get("keywords", "")  # 查询关键词
    page_num = request.GET.get("page_num", 1)  # 页码
    # 查询用户
    user_id = request.COOKIES.get("user_id")
    print(user_id,"user_id")
    #store = Store.objects.get(id=int(store_id))
    seller = Seller.objects.get(id=int(user_id))  # 根据id获取对应店铺的对象
    print(seller,"seller")
    if keywords:#store店铺表没有外键user_id同过cookie获取用户名
        #goods_list = store.goods_set.filter(goods_under=state_num, goods_name__contains=keywords)
        store_list=Store.objects.filter(user_id=int(user_id),store_name__contains=keywords)# 完成了模糊查询
    else:
        store_list = Store.objects.filter(user_id=int(user_id))
    paginator=Paginator(store_list,3)#分页，每页3条数据
    page_num = int(page_num)
    page = paginator.page(int(page_num))
    if len(store_list) / 3 <= page_num - 1:
        if page_num >= 2:
            page_num -= 1
        else:
            page_num = 1
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/store_list.html", locals())
def  choose(request):#店铺选择
    store_id = request.GET.get("store_id")
    response=HttpResponseRedirect("/store/store_list/?store_id="+store_id)
    response.set_cookie('has_store', store_id)
    return response











