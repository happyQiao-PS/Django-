import time

from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class study(MiddlewareMixin):
    def process_request(self,request):

        # #跳过csrf验证
        # request.csrf_processing_done = True
        #
        # ip = request.META.get("REMOTE_ADDR")
        # requests = cache.get(ip,[])
        # black = cache.get("black",[])
        #
        # if ip in black:
        #     return HttpResponse("你被拉黑了")
        #
        # if requests and time.time()-requests[-1]>60:
        #     requests.pop()
        #
        # requests.insert(0,time.time())
        # cache.set(ip,requests,timeout=60)
        #
        # if len(requests)>30:
        #     cache.set("black",ip)
        #
        # if len(requests)>10:
        #     return HttpResponse("不要在访问了！")
        pass

