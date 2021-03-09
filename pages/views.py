from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello Summaiya</h1>")
    return render(request, "home.html", {})

def contact_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello Contact</h1>")
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello Contact</h1>")
    return render(request, "about.html", {})

def expression_view(request):
    a = int(request.POST['text1'])
    b = int(request.POST['text2'])
    c = a + b
    return render(request, "output.html", {"result": c})

    