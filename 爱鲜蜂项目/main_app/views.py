import re
import uuid

from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from main_app.hanshuModel import DEFAULT_ORDER, SALES_MUCH, MUCH_PRICE, LESS_PRICE, send_email, select_price, \
    SUBMIT_NOT_PAY, SUBMIT_ALREADY_PAY, SUBMIT_PAYED_REACH
from main_app.models import axf_foodtypes, axf_goods, axf_user, axf_shopping_cart, axf_order, axf_ordergoods


def home(request):
    data={
        "title":"主页",
    }
    return render(request,"main/home.html",context=data)


def market(request):
    typeid = request.GET.get("typeid")
    cid = request.GET.get("cid")
    order = request.GET.get("order")
    if typeid and typeid!="0":
        goods = axf_goods.objects.filter(categoryid=typeid)
    else:
        goods = axf_goods.objects.all()
        typeid = 104749
    if cid and cid != 'None' and cid !="0":
        goods = goods.filter(childcid=cid)
    types = axf_foodtypes.objects.all()

    if order==SALES_MUCH:
        goods = goods.order_by("productnum")
    elif order==MUCH_PRICE:
        goods = goods.order_by("-price")
    elif order==LESS_PRICE:
        goods = goods.order_by("price")


    #排序方法数据的列表
    order_way_list = [["默认排序",DEFAULT_ORDER], ["销量排序", SALES_MUCH], ["高价排序", MUCH_PRICE], ["低价排序", LESS_PRICE]]

    '''全部分类: 0  # 进口水果:103534#国产水果:103533'''
    child_item_list = [item.split(":") for item in types.get(typeid=typeid).childtypenames.split("#")]
    data = {
        "title": "商品列表",
        "types": types,
        "goods":goods,
        "typeid":int(typeid),
        "child_item_list":child_item_list,
        "order_way_list":order_way_list,
        "order":order,
        "cid":cid,
    }
    return render(request, "main/market.html", context=data)


def cart(request):
    s_price = 0
    uid = request.uid if request.uid else 0
    cart = axf_shopping_cart.objects.filter(s_good__axf_shopping_cart__s_user_id=uid)
    is_select_all = not cart.filter(s_isChoice=False).exists()
    s_price = select_price()
    data = {
        "title": "购物车",
        "is_select_all":is_select_all,
        "s_price":s_price,
    }
    if cart.exists():
        data["cart"] = cart
    return render(request, "main/cart.html", context=data)

def register(request):
    if request.method=="GET":
        return render(request,"user/register.html")
    elif request.method=="POST":
        #获取数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        icon = request.FILES.get("icon")
        user = axf_user()
        user.u_username = username
        user.u_password = make_password(password)
        user.u_email = email
        user.u_icon = icon
        user.save()
        return redirect(reverse("axf:goToActivate")+"?username="+username)

def login(request):
    if request.method=="GET":
        if request.GET.get("key") and request.GET.get("key")=="0":
            return render(request,"user/login.html",{"key":"0"})
        return render(request,"user/login.html")
    elif request.method=="POST":
        key = False
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        #usernameorpassword即有可能是用户名也有可能是邮箱地址
        #这个user就是目标的对象
        user = axf_user.objects.filter(u_username=username_or_email).first() if axf_user.objects.filter(u_username=username_or_email).exists() else axf_user.objects.filter(u_email=username_or_email).first()
        if user:
            key = True if check_password(password,user.u_password) else False
        if key:
            request.session["user"] = user.id
        else:
            return redirect(reverse("axf:login") + "?key=" + str(0))
        return redirect(reverse("axf:mine"))


def goToActivate(request):
    username = request.GET.get("username")
    user = axf_user.objects.filter(u_username=username).first()
    email = user.u_email
    u_token = uuid.uuid4().hex
    send_email(u_token,email,username)
    return render(request, "activate/response.html")

#激活
def activate(request):
    u_token = request.GET.get("u_token")
    username = request.GET.get("name")
    if u_token and username:
        cache.set(username,u_token,timeout=(60*60*12))
        user = axf_user.objects.filter(u_username=username).first()
        user.u_isactivate = 1
        user.save()
    return redirect(reverse("axf:login"))


def mine(request):
    data = {
        "title": "我的",
        "user": False,
    }
    try:
        key = request.session["user"]
    except:
        key = False
    if key:
        user = axf_user.objects.get(pk=key)
        data["user"] = user
        data["cache_style"] = cache.get(user.u_username)
        data["order_not_pay_count"] = axf_order.objects.filter(o_order_statu=SUBMIT_NOT_PAY).count()
        data["order_payed_not_recv"] = axf_order.objects.filter(o_order_statu__in=[SUBMIT_ALREADY_PAY,SUBMIT_PAYED_REACH]).count()
    return render(request, "main/mine.html", context=data)


def quit_login(request):
    request.session.flush()
    return redirect("axf:mine")


def register_check_username(request):
    data={"data":"200"}
    username = request.GET.get("username")
    user = axf_user.objects.filter(u_username=username)
    if user.exists():
        data["data"] = "404"
    return JsonResponse(data)


def register_check_email(request):
    data = {"data": "200"}
    email = request.GET.get("email")
    user = axf_user.objects.filter(u_email=email)
    if user.exists():
        data["data"] = "404"
    return JsonResponse(data)

@csrf_exempt
def add_to_shopping_cart(request):
    goodid = request.POST.get("goodid")
    userid = request.uid
    key = request.POST.get("key")
    if goodid and userid:
        good = axf_goods.objects.get(pk=goodid)
        user = axf_user.objects.get(pk=userid)
        if good and user:
            cart_ext = axf_shopping_cart.objects.filter(s_good=good).filter(s_user=user)
            if cart_ext.exists():
                cart_ext = cart_ext.first()
                if key=="-" and cart_ext.s_num > 0:
                    cart_ext.s_num = int(cart_ext.s_num) - 1
                elif key=="+":
                    cart_ext.s_num = int(cart_ext.s_num) + 1
                elif key=="-" and cart_ext.s_num == 0:
                    cart_ext.delete()
                cart_ext.save()
                data = {
                    "login-statu": "Login OK",
                    "choice_num": cart_ext.s_num,
                }
            else:
                cart = axf_shopping_cart()
                cart.s_good = good
                cart.s_user = user
                if key=="+":
                    cart.s_num = 1
                elif key=="-":
                    cart.s_num = 0
                cart.s_isChoice = True
                cart.save()
                data = {
                    "login-statu": "Login OK",
                    "choice_num": cart.s_num,
                }
            return JsonResponse(data)
    return HttpResponse("未知错误")


def selected(request):
    s_price = 0
    data = {}
    cartid = request.GET.get("cartid")
    try:
        cart = axf_shopping_cart.objects.get(pk=cartid)
        cart.s_isChoice = not cart.s_isChoice
        cart.save()
        data["key"]= cart.s_isChoice
    except:
        pass
    select_all = not axf_shopping_cart.objects.filter(s_user_id=request.uid).filter(s_isChoice=False).exists()
    data["select_all"] = select_all
    data["s_price"] = select_price()
    return JsonResponse(data=data)

@csrf_exempt
def change_cart_num(request):
    data = {
        "login-statu": "Login OK",
        "choice_num": 0,
        "s_price":select_price(),
    }
    key = request.POST.get("key")
    cartid = request.POST.get("cartid")
    try:
        cart = axf_shopping_cart.objects.get(pk=cartid)
        if key=="+":
            cart.s_num = int(cart.s_num) + 1
            cart.save()
            data["choice_num"] = cart.s_num
        elif key=="-" and cart.s_num <= 0:
            cart.delete()
        elif key=="-" and cart.s_num > 0 :
            cart.s_num = int(cart.s_num) - 1
            cart.save()
            data["choice_num"] = cart.s_num
        data["s_price"] = select_price()
        return JsonResponse(data=data)
    except:
        return JsonResponse(data=data)


def select_all(request):
    unselect_list = request.GET.get("unselect_list").split("#")
    cart = axf_shopping_cart.objects.filter(id__in=unselect_list)
    for cart_item in cart:
        cart_item.s_isChoice = not cart_item.s_isChoice
        cart_item.save()
    data = {
        "statu":"good",
        "s_price":select_price(),
    }
    return JsonResponse(data=data)


def submitOrder(request):
    #先创建相应的订单，然后在为订单添加商品数据
    order = axf_order()
    order.o_user = axf_user.objects.get(pk=request.uid)
    order.o_price = select_price()
    order.o_order_statu = SUBMIT_NOT_PAY
    order.save()
    select_carts = axf_shopping_cart.objects.filter(s_isChoice=True)
    for cart in select_carts:
        ordergood = axf_ordergoods()
        ordergood.og_order = order
        ordergood.og_goods = cart.s_good
        ordergood.og_num = cart.s_num
        ordergood.save()
        cart.delete()
    data = {
        "title":"订单详情",
        "order":order,
    }
    return render(request,"order/submit.html",context=data)


def submit_not_payed(request):
    title = "未付款"
    try:
        orders = axf_order.objects.filter(o_user=axf_user.objects.get(pk=request.uid)).filter(o_order_statu=SUBMIT_NOT_PAY)
    except:
        pass
    return render(request,"order/submit_not_payed.html",context=locals())


def payed(request):
    orderid = request.GET.get("orderid")
    order = axf_order.objects.get(pk=orderid)
    order.o_order_statu = SUBMIT_ALREADY_PAY
    order.save()
    data={
        "msg":"OK"
    }
    return JsonResponse(data=data)


def submit_not_recv(request):
    title="未收货"
    try:
        orders = axf_order.objects.filter(o_user=axf_user.objects.get(pk=request.uid)).filter(o_order_statu__in=[SUBMIT_ALREADY_PAY,SUBMIT_PAYED_REACH])
    except:
        pass
    return render(request, "order/submit_not_payed.html", context=locals())