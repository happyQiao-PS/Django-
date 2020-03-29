from django.core.mail import send_mail


#["默认排序",1],["销量排序",2],["高价排序",3],["低价排序",4]
from django.template import loader

from main_app.models import axf_shopping_cart

DEFAULT_ORDER = "1"
SALES_MUCH = "2"
MUCH_PRICE = "3"
LESS_PRICE = "4"

def send_email(u_token,email,username):
    subject = "激活邮件"
    msg = loader.get_template("activate/activate.html").render(locals())
    send_mail(
        subject=subject,
        message="",
        html_message=msg,
        from_email='2945887050@qq.com',
        recipient_list = [email,],
        fail_silently=False,
    )

def select_price():
    select_price = 0
    select_carts = axf_shopping_cart.objects.filter(s_isChoice=True)
    for cart in select_carts:
        select_price += cart.s_good.price*cart.s_num
    return "{:.2f}".format(select_price)

#订单的状态
SUBMIT_NOT_PAY = 1

SUBMIT_ALREADY_PAY = 2

SUBMIT_PAYED_REACH = 3