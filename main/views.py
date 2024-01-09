from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ping(request):
    print('Successfully pinged the site.')
    return HttpResponse('Ok')