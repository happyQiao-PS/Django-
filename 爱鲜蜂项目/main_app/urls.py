from django.conf.urls import url

from main_app import views

urlpatterns = [
    # 页面下面的四个按钮
    url(r"^home/", views.home, name="home"),
    url(r"^market/", views.market, name="market"),
    url(r"^cart/", views.cart, name="cart"),
    url(r"^mine/", views.mine, name="mine"),

    # 注冊主鍵的路由
    url(r"^register/", views.register, name="register"),
    url(r"^login/", views.login, name="login"),
    url(r"^quit_login/", views.quit_login, name="quit_login"),

    # 前端ajax请求的url位置以及响应
    url(r"^register_check_username/", views.register_check_username, name="register_check_username"),
    url(r"^register_check_email/", views.register_check_email, name="register_check_email;"),
    url(r"^add_to_shopping_cart/", views.add_to_shopping_cart, name="add_to_shopping_cart"),
    url(r"^change_cart_num/", views.change_cart_num, name="change_cart_num"),

    # 负责激活的逻辑接口
    url(r"^activate/", views.activate, name="activate"),
    url(r"^goToActivate/", views.goToActivate, name="goToActivate"),

    # 负责购物车商品选中逻辑的接口
    url(r"^selected/", views.selected, name="selected"),
    url(r"^selectall/", views.select_all, name="select_all"),

    # 提交订单
    url(r"^submitOrder/", views.submitOrder, name="submitOrder"),

    url(r"^submit_not_payed", views.submit_not_payed, name="submit_not_payed"),
    url(r"^submit_not_recv", views.submit_not_recv, name="submit_not_recv"),
    url(r"^payed", views.payed, name="payed"),
]
