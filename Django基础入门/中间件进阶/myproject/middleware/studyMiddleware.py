import time

from django.core.cache import cache

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin



class studyMiddleware(MiddlewareMixin):
    def process_request(self,request):
        ip = request.META.get("REMOTE_ADDR")
        requests = cache.get(ip,[])
        if requests and time.time()-requests[-1]>60:
            requests.pop()
        if len(requests)>9:
            return HttpResponse("等一下在回来访问吧")
        requests.insert(0,time.time())
        cache.set(ip,requests,timeout=60)
