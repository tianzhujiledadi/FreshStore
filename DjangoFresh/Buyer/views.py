from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from  Buyer.models import *
from  Store.views import setpw
from  Store.models import *
from django.db.models import Sum
# Create your views here.
def  loginValid(fun):
    def  inner(request,*args,**kwargs):
        c_user=request.COOKIES.get("username")
        s_user=request.session.get('username')
        print(c_user)
        print(s_user)
        if  c_user and s_user and c_user==s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buyer/login/")
    return inner
@loginValid
def  index(request):
    result_list=[]
    goodstypelist=GoodsType.objects.all()
    for goodstype in  goodstypelist:
        goodlist=goodstype.goods_set.values().filter(goods_under=1)[:4]
        #筛选有goodstype对应的goods中goods_under=1的goods对象
        if goodlist:
            goodsType={
                "id": goodstype.id,
                "name":goodstype.name,
                "description":goodstype.description,
                "picture":goodstype.picture,
                "goodlist":goodlist
            }
            result_list.append(goodsType)
    return render(request,'buyer/index.html',locals())
def  base(request):
    return render(request,'buyer/base.html')
def  register(request):
    if request.method=='POST':
        username=request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        buyer=Buyer()
        buyer.username=username
        buyer.password=setpw(password)
        buyer.email=email
        buyer.save()
        return HttpResponseRedirect('/buyer/login/')
    return render(request,'buyer/register.html')
def login(request):
    if  request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        if  username  and  password:
            user=Buyer.objects.filter(username=username).first()
            if user:
                web_password=setpw(password)
                if  web_password==user.password:
                    response=HttpResponseRedirect("/buyer/index/")
                    response.set_cookie("username",user.username)
                    response.set_cookie("user_id",user.id)
                    request.session['username']=username
                    return response
    return  render(request,"buyer/login.html",locals())
def  logout(request):
    response=HttpResponseRedirect("/buyer/login/")
    for key  in  request.COOKIES:
        response.delete_cookie(key)
    del  request.session["username"]
    return response
@loginValid
def  goods_list(request):
    goodsList=[]
    print("type_id")
    type_id=request.GET.get("type_id")
    print(type_id)
    #获取类型
    goods_type=GoodsType.objects.filter(id=type_id).first()
    print(goods_type)
    if goods_type:#goods_under是上线状态1是上线；0是下线
        goodsList=goods_type.goods_set.filter(goods_under=1)
        print(goodsList)
    goodsList2=goodsList[:2]
    return  render(request,"buyer/goods_list.html",locals())
# def  detail(request):
#     id=request.GET.get("goods_id")
#     goods=Goods.objects.filter(id=id).first()
#     goodsList = []
#     type_id = request.GET.get("type_id")
#     goods_type = GoodsType.objects.filter(id=type_id).first()
#     if goods_type:  # goods_under是上线状态1是上线；0是下线
#         goodsList = goods_type.goods_set.filter(goods_under=1)
#     goodsList2 = goodsList[:2]
#     count = 1#商品默认购买数量
#     inventory = "库存:%d"%(goods.goods_number)  # 商品库存
#     priceall = int(goods.goods_price)*count
#     return render(request, "buyer/detail.html", locals())
def detail(request):
    id = request.GET.get("goods_id")
    goods=Goods.objects.filter(id=id).first()
    inventory = goods.goods_number  # 商品库存
    return render(request, "buyer/detail.html", locals())
import time
def setOrderId(user_id,goods_id,store_id):
    """设置商品订单编号
    时间+用户id+商品id+店铺id"""
    strftime=time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strftime+user_id+goods_id+store_id#拼接字符串
def  place_order(request):
    if request.method=="POST":
        #POST数据
        count=int(request.POST.get("count"))
        goods_id=request.POST.get("goods_id")
        user_id=request.COOKIES.get("user_id")#通过cookie获取
        goods=Goods.objects.get(id=goods_id)
        store_id=goods.store_id.id#获取商品对应的商店的id
        #store_id=15
        order=Order()#订单表
        order.order_id=setOrderId(str(user_id),str(goods_id),str(store_id))#设置订单编号
        order.goods_count=count
        order.order_user=Buyer.objects.get(id=user_id)#获取用户id
        order.order_price=count*goods.goods_price
        order.order_status=1#设置订单状态为未支付
        order.save()
        order_detail=OrderDetail()#订单详情表
        order_detail.order_id=order
        order_detail.goods_id=goods.id
        order_detail.goods_price=goods.goods_price
        order_detail.goods_number=count
        order_detail.goods_name = goods.goods_name
        order_detail.goods_total = count*goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image=goods.goods_image
        order_detail.save()
        detail=[order_detail]
        return render(request,"buyer/place_order.html",locals())
    else:
        order_id=request.GET.get("order_id")
        if order_id:
            order=Order.objects.get(id=order_id)
            detail=order.orderdetail_set.all()
            return render(request,"buyer/place_order.html",locals())
        return HttpResponse('666666666666')
from django.http import JsonResponse#json+httpresponse
from django.core.paginator import Paginator#引入分页模块
def  cart(request):#购物车页面
    user_id=request.COOKIES.get("user_id")
    goods_list=Cart.objects.filter(user_id=user_id).order_by("-id")
    page_num = request.GET.get("page_num", 1)  # 默认是第一页
    paginator = Paginator(goods_list, 3)  # 将获取的所有数据按每页3条数据分页
    page_num = int(page_num)
    if len(goods_list) / 3 <= page_num - 1:
        if page_num >= 2:
            page_num -= 1
        else:
            page_num = 1
    page = paginator.page(int(page_num))
    page_range = paginator.page_range  # 获取所有页码
    return render(request, "buyer/cart.html", locals())
    if request.method=="POST":#cart页提交订单
        post_data=request.POST
        cart_data=[]#收集前端传递过来的商品
        cart_ids=[]
        for k,v in post_data.items():
            if k.startswith("goods_"):#判断传过来的订单id
                print(v,"v",k,"k")
                cart_data.append(Cart.objects.get(id=int(v)))
                cart_ids.append(int(v))
        goods_count=sum([int(i.goods_number) for i in cart_data])#提交过来的数据总的数量
        #goods_total=sum([int(i.goods_total) for i in cart_data])#订单的总价
        goods_total=Cart.objects.filter(id__in=cart_ids).aggregate(Sum("goods_total"))#得到一个字典
        goods_total=goods_total["goods_total__sum"]
        #goods_store=([str(i.goods_store) for i in cart_data])
        #保存订单
        order=Order()
        order.order_id=setOrderId(str(user_id),str(goods_count),"2")
        #订单中有多个商品或者多个店铺，使用goods_count来代替商品id,使用2代表店铺id
        order.goods_count=goods_count
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_price=goods_total
        order.order_status=1
        order.save()
        #保存订单详情
        #这里的detail是购物车里的数据实例，不是商品的实例
        for detail in cart_data:
            order_detail=OrderDetail()
            order_detail.order_id=order#order是一条订单数据
            order_detail.goods_id = detail.goods_id
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_number = detail.goods_number
            order_detail.goods_total = detail.goods_total
            order_detail.goods_store = detail.goods_store
            order_detail.goods_image = detail.goods_picture
            order_detail.save()
        url="/buyer/place_order/?order_id=%s"%order.id
        return HttpResponseRedirect(url)

def  add_cart(request):
    result={"state":"error","data":""}
    if request.method=="POST":
        print("跳转成功")
        count=int(request.POST.get("count"))#request请求
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.filter(id=goods_id).first()
        user_id=request.COOKIES.get("user_id")#cookie数据
        cart=Cart()
        cart.goods_name=goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price*count
        cart.goods_number=count
        cart.goods_picture=goods.goods_image
        cart.goods_id=goods_id
        cart.goods_store = goods.store_id.id
        cart.user_id=user_id
        cart.save()
        result["state"]="success"
        result["data"]="商品添加成功"
        return HttpResponseRedirect("/buyer/cart/")
    else:
        result["data"]="请求错误"
    return JsonResponse(result)

##############################################################################################################
from  alipay import AliPay
def  pay_order(request):
    money=request.GET.get("money")
    order_id=request.GET.get("order_id")
    print(money)
    print(order_id)
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsNlcDS8XlMdOFGHSpMf0G4RVfGhJy/nhX3bm//PgPcFRv9M3eCP7zBO+gwBTdcLy0XVc/8o6DC6Hc+xy4UtSm7+LJu0Y2rN9E/uz6gXKtrYNkIZY9EFfp39oSM3ofip49BM+3p9dHd7w1HtF9lq2L4Yt+fpixr3vreciy5swHiDO8vEC17XdvQqda5NUblxSKt/QDF1so870Tl695y9QFU+DsXfpY2HeSCJIdMgsFzhs8rhzIT2vzOALTgOuWPxIQzAG5iaiktZSiJAV3N8Www7beYlCrjIvh/zaj/F1Ai5nxjoW5VUjiU7nDU7aYBKvpnkjXLh10xZqwZhsHx3uwQIDAQAB
    -----END PUBLIC KEY-----"""
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAsNlcDS8XlMdOFGHSpMf0G4RVfGhJy/nhX3bm//PgPcFRv9M3eCP7zBO+gwBTdcLy0XVc/8o6DC6Hc+xy4UtSm7+LJu0Y2rN9E/uz6gXKtrYNkIZY9EFfp39oSM3ofip49BM+3p9dHd7w1HtF9lq2L4Yt+fpixr3vreciy5swHiDO8vEC17XdvQqda5NUblxSKt/QDF1so870Tl695y9QFU+DsXfpY2HeSCJIdMgsFzhs8rhzIT2vzOALTgOuWPxIQzAG5iaiktZSiJAV3N8Www7beYlCrjIvh/zaj/F1Ai5nxjoW5VUjiU7nDU7aYBKvpnkjXLh10xZqwZhsHx3uwQIDAQABAoIBAA4YFIz8bs2toJxhO29kfCDhSArVKOR3sq1wBXLqlbl2ObSm+am6fGvEOw+nq/8bnUxyJQpBrKSh5KupcXJhFWFSP53HkY6EdXhtO+ZvtbsgAS6+dkJpH11y+vWqa1f6vI7/JaiKXNpvlRPqCyZaDmD1OZ7NhKfAJWTfoddGM+yCoM4fOSJekSXLuZYOLEFWJ/hzTfvp15T0PkDh00KxGGMEEvV0yqUKUIjViv7O8K8Aks7W5rKmUikAp6CpcahoEoGA3TeyH+womvNvYmw8iu/9z19SoAtwObG4jVRvE3/Wtsy0fJqJNj5mOiemeaEgjrGcaKORolM2ZS7XWpZgVdECgYEA6NXrSVtQMH0HL0YbYpVTlGx0xc9jb1VyZJ2ryZWMzpDZBdjVZ/7XGkJE8dCPYb+6ouUV+Bs97n/u5h0J/UcxOTnvrJaKzIzQ74V/HadbG340i6nDhli0p2M2pjOM4n882Yvlm+YVUOz9nuyuY4b/kI3TX4vJgd/0DCbA+2RnT9UCgYEAwnGFZLYzBR1Ey9Klj77wRKZKLejghuX4amJrfCkIpa8uMnxajEg2xs810SjCQCALQL6v+2m91zGmd1K+EzPrjy3x2JexB13gkmgRUdM+hSsI5/5V9z7htbqyJ8PXalL/WKKRlfQh1kG3ct+nBLbBeRPjXPxlOpYek3q2CnNNxT0CgYAIKDZuA3zzte2iglpDQegDsykEJRfetqejTsLN9SdRtVFlGwue8RaoHNo9fokHa6gmPNBgONQanvDHrwzCitP2pUj4Su3h7K0FNzAU4eAXPnyox/HJqyHpG1i2yeeNp9eB55zLsWvdwe/AuZoCcqBReCaHmmYc3rO2GUV5iTL1YQKBgCnp7JY0DDVrBLxm8NdWklZJ/i19SIDrq6vLAV5nPfzxESVC1wXsPxqF6hTnE1BdV++h6y9nsMtlYXvRMzXSeFGJ1tsYf8mVu+XzVuBrh8uO5kGT+pXsUR0qXGLj/VhnAbHqgTVwxaZ4zgGOImOKvZPK7LTLl0qUt4yU5A7GohoFAoGACCyrRGFTAyzcAV6jYsK+neRxmJogUV/zjzoohnU8eDH1v9Efehos0ixA2igPw7aTXE/D+foFbqC6SPGDp+NFeyVm/u04nlVXNKznN6w5MOG3up6iTuszs6yicZVenytENqwPCidYr0mQW4htSfZgzQG7hXkoYu9xv8b2rAFaMO8=
    -----END RSA PRIVATE KEY-----"""
    # 实例化支付应用
    alipay = AliPay(
        appid="2016093000627799",
        app_notify_url=None,  # 应用程序url通知
        app_private_key_string=app_private_key_string,  # 私钥
        alipay_public_key_string=alipay_public_key_string,  # 公钥
        sign_type="RSA2"  # 加密算法
    )
    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(  # 网页支付请求
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主体
        return_url='http://127.0.0.1:8000/buyer/pay_result/',
        notify_url='http://127.0.0.1:8000/buyer/pay_result/'
        # notify通知公告,notify通知公告，notify
    )
    order=Order.objects.get(order_id=order_id)
    order.order_status=2#将订单状态改为未支付
    order.save()
    return  HttpResponseRedirect("http://openapi.alipaydev.com/gateway.do?" + order_string)
def  pay_result(request):
    # qie="http://127.0.0.1:8000/buyer/pay_result/?charset=utf-8&out_trade_no=36966&method=alipay.trade.page.pay.return&total_amount=636363.00&sign=TenqHQz1D2E%2BMP2MGD77p%2BUSbyxJrYp27cFPwlZ9Mm%2FJPHTMTMvJS5%2BIlLsqR82qLVzuvq7TUXaHBzVilfZUtCgmz3wUP1WH%2B%2B1tDsdVwBzwZ0IpM0ngXSwmDqEYPa7UKylXDb6m7bPySro9uahrmK2G3n1Y%2Bvta1Shmrqip%2BzvWH%2FkApeS2jB1DDJ8je1LQsOc0ZMdbtZvbQa%2BtQWdiScUWuXJG5NatuXuYIlCNo2gnznO22wf%2FAWfWsvGUi4Pdt86RomEGJKOCiH8HPoE3ksNJuF299pv3Uv%2FoCjF8hUamND773gZnarQ1Nt1%2Bh25gjLE2cII3eC7Op2oBW0isEg%3D%3D&trade_no=2019072622001451791000025531&auth_app_id=2016093000627799&version=1.0&app_id=2016093000627799&sign_type=RSA2&seller_id=2088102177880794&timestamp=2019-07-26+19%3A23%3A28"
    # trade_no=###订单号
    # auth_app_id=###用户的应用id
    # version=1.0#版本
    # app_id=###商家的应用id
    # sign_type=RSA2#加密方式
    # seller_id=###商家id
    # timestamp=2019-07-26#时间
    return  render(request,"buyer/pay_result.html",locals())
import  datetime
def TestGoods(request):#添加商品
    goods_type=GoodsType.objects.all()
    sg = "杏、樱桃、桃、水蜜桃、油桃、黑莓、覆盆子、云莓、罗甘莓、白里叶莓、橘子、砂糖桔、橙子、柠檬、青柠、柚子、金桔、葡萄柚、香橼、佛手、指橙、黄皮果、蟠桃、李子、梅子、青梅、西梅、白玉樱桃"
    znyr = "猪肉、猪腿、大肠、羊肉、羊蹄、羊头、羊杂、牛板筋、牛肉、牛排"
    hxsc = "巴沙鱼、虾仁、三文鱼、长尾鳕、白虾、北极甜虾、大黄鱼、海鳝鱼、美国红黑虎虾"
    qldl = "乌骨鸡、绿壳蛋乌鸡、榛鸡、黑凤鸡、白来航鸡、安得纽夏鸡、黑米诺卡鸡、洛岛红鸡、黑狼山鸡、新汗夏、芦花鸡、浅花苏塞克斯、澳洲黑、九斤黄鸡、七彩山鸡"
    store=Store.objects.get(id=15)#获取店铺等于15
    # for  f in  znyr.split("、"):
    #     goods=Goods()
    #     goods.goods_name=f
    #     goods.goods_price=9000.00
    #     goods.goods_image="buyer/images/banner01.jpg"
    #     goods.goods_number=60
    #     goods.goods_description=f
    #     goods.goods_date=datetime.datetime.now()
    #     goods.goods_safeDate=1
    #     goods.goods_under=1
    #     goods.goods_type=goods_type[3]
    #     goods.store_id=store
    #     goods.save()
    # for z in sg.split("、"):
    #     goods = Goods()
    #     goods.goods_name = z
    #     goods.goods_price = 6000.00
    #     goods.goods_image = "buyer/images/banner03.jpg"
    #     goods.goods_number = 60
    #     goods.goods_description = z
    #     goods.goods_date = datetime.datetime.now()
    #     goods.goods_safeDate = 1
    #     goods.goods_under = 1
    #     goods.goods_type = goods_type[0]
    #     goods.store_id = store
    #     goods.save()
    # for h in hxsc.split("、"):
    #     goods = Goods()
    #     goods.goods_name = h
    #     goods.goods_price = 18000.00
    #     goods.goods_image = "buyer/images/banner02.jpg"
    #     goods.goods_number = 60
    #     goods.goods_description = h
    #     goods.goods_date = datetime.datetime.now()
    #     goods.goods_safeDate = 1
    #     goods.goods_under = 1
    #     goods.goods_type = goods_type[1]
    #     goods.store_id = store
    #     goods.save()
    for q in qldl.split("、"):
        goods = Goods()
        goods.goods_name = q
        goods.goods_price = 12000.00
        goods.goods_image = "buyer/images/banner04.jpg"
        goods.goods_number = 60
        goods.goods_description = q
        goods.goods_date = datetime.datetime.now()
        goods.goods_safeDate = 1
        goods.goods_under = 1
        goods.goods_type = goods_type[6]
        goods.store_id = store
        goods.save()
    return HttpResponse("商品添加成功")
def goodsexit(request):
    goods = Goods.objects.order_by("id")
    for i in range(len(goods)):
        goods[i].id=i
    # goods = Goods.objects.filter(goods_image="buyer/banner01.jpg")
    # for good in goods:
    #     good.goods_image="buyer/images/banner01.jpg"
    #     good.save()
    # goods = Goods.objects.filter(goods_image="buyer/banner03.jpg")
    # for good in goods:
    #     good.goods_image="buyer/images/banner03.jpg"
    #     good.save()
    # goods = Goods.objects.filter(goods_image="buyer/banner02.jpg")
    # for good in goods:
    #     good.goods_image="buyer/images/banner02.jpg"
    #     good.save()
    # goods = Goods.objects.filter(goods_image="buyer/banner04.jpg")
    # for good in goods:
    #     good.goods_image="buyer/images/banner04.jpg"
    #     good.save()
    return HttpResponseRedirect('/buyer/index/')






