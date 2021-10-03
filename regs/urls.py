from django.urls import path

from . import views

app_name="regs"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:reg_id>', views.reg, name="reg"),
    path('<int:reg_id>/book', views.book, name="book"),
    path('<int:reg_id>/remove', views.remove, name="remove"),
]