from django.http import HttpResponse
def hehe(request):
    return HttpResponse("hehe")
def hehehe(request,suzi):
    return HttpResponse("hehehe %s" %suzi)
def hehehe1(request,suzi,zimu):
    return HttpResponse("hehehe %s %s" %(suzi,zimu))