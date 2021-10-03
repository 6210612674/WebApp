from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from regs.models import Reg

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")

def username_view(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html",{
                "message": "Invalid Credential."
            })

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html",{
        "message": "Logged out."
    })

def results(request):
    courselist = []
    for c in Reg.objects.all():
        if request.user in c.students.all():
            courselist.append(c)
    return render(request, "users/result.html",{
            "courselist": courselist
    })