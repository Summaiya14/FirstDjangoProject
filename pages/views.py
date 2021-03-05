from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return HttpResponse("<h1>Hello Summaiya</h1>")

def contact_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello Contact</h1>")

