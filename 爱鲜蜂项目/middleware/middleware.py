from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from main_app.models import axf_shopping_cart

ACCEPT_ITERFACE_LIST_JSON = ['/axf/add_to_shopping_cart/','/axf/payed/']
ACCEPT_ITERFACE_LIST = ['/axf/cart/', '/axf/selected/','/axf/change_cart_num/','/axf/submitOrder/','/axf/submit_not_payed/','/axf/submit_not_recv/']


class Mymiddleware(MiddlewareMixin):
    def process_request(self,request):
        #在中间件加载的时候优先判断数据库中是否存在死数据，如果有，就干掉
        cart = axf_shopping_cart.objects.filter(s_num=0)
        if cart.exists():
            for cart_item in cart:
                cart_item.delete()
        #这里的接受逻辑专指前段ajax发送到后端的数据逻辑，是需要响应的逻辑
        if request.path in ACCEPT_ITERFACE_LIST_JSON:
            try:
                uid = request.session["user"]
            except:
                uid = False
            if uid:
                request.uid = uid
            else:
                return JsonResponse({
                    "login-statu":"Not Login",
                })
        #这里的逻辑值得是购物车本生的逻辑，如果你试图加载进入购物车的页面，那么你就需要确定自己是否登录
        if request.path in ACCEPT_ITERFACE_LIST:
            try:
                uid = request.session["user"]
            except:
                uid = False
            if uid:
                request.uid = uid
            else:
                return redirect(reverse("axf:login"))



