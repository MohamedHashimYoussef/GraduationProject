from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Create your views here.

def index(request):
    return render(request, "static_pages/index.html")
@csrf_exempt
def skin(request):
    return HttpResponse('false')

@csrf_exempt
def malaria(request):

    return HttpResponse('false')

@csrf_exempt
def brain(request):

    return HttpResponse('false')
