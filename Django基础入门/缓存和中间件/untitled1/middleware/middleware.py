import random

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class getPhone(MiddlewareMixin):
    def process_request(self,request):
        ip = request.META.get("REMOTE_ADDR")
        print(ip)
        if ip=="192.168.1.1" and random.randrange(100)>20:
            return HttpResponse("恭喜您抢到了一部小米手机！")