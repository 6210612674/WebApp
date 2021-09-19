from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.

from .models import *


def index(request):
    return render(request, "regs/index.html", {
        "regs": Reg.objects.all(),
        "students": Reg.objects.all(),
    })

def reg(request, reg_id):
    reg = get_object_or_404(Reg, pk=reg_id)
    return render(request, "regs/reg.html",{
        "reg": reg,
        "student": reg.students.all(),
        "count": reg.students.all().count(),
    })


def book(request, reg_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("users:login")+f"?next={request.path}", {"messages": messages.get_messages(request),})

    reg = get_object_or_404(Reg, pk=reg_id)
    if request.user not in reg.students.all():
        reg.students.add(request.user)
    return HttpResponseRedirect(reverse("regs:index"))


def remove(request, reg_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("users:login")+f"?next={request.path}", {"messages": messages.get_messages(request),})

    reg = get_object_or_404(Reg, pk=reg_id)
    if request.user in reg.students.all():
        reg.students.remove(request.user)
    return HttpResponseRedirect(reverse("regs:index"))
