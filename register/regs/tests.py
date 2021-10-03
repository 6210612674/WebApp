from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import *
from regs.models import User
import datetime


# Create your tests here.


class RegViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="user1", password="1234", email="user1@example.com")
        reg = Reg.objects.create(course_status=1, course_code='CN210', course_name='Architecture', course_semester='2', course_quota=5)
        reg.students.add(user)
        reg.save()


    def test_quota_full(self):
        user = User.objects.get(username="user1")
        reg = Reg.objects.create(course_status=1, course_code='CN103', course_name='Introduction to Java', course_semester='2', course_quota=1)
        reg.students.add(user)
        reg.save()

        self.assertEqual(reg.__str__(), f"CN103 Introduction to Java 2/{datetime.date.today().year+543}  [Quota : FULL ]")


    def test_index(self):
        reg = Reg.objects.get(course_code='CN210')
        c = Client()
        response = c.get(reverse('regs:index'))
        self.assertEqual(response.status_code, 200)


    def test_reg(self):
        reg = Reg.objects.get(course_code='CN210')
        c = Client()
        r = Reg.objects.first()
        response = c.get(reverse('regs:reg', args=(r.id,)))
        self.assertEqual(response.status_code, 200)


    def test_guest_user_cannot_book(self):
        user = User.objects.create(username="user2", password="1234", email="user2@example.com")
        r = Reg.objects.first()
        c = Client()
        response = c.get(reverse('regs:book', args=(r.id,)))
        self.assertEqual(r.students.count(), 1)


    def test_authenticated_user_can_book(self):
        user = User.objects.create(username="user2", password="1234", email="user2@example.com")
        r = Reg.objects.first()
        r.capacity = 2
        r.save
        c = Client()
        c.force_login(user)
        response = c.get(reverse('regs:book', args=(r.id,)))
        self.assertEqual(r.students.count(), 2)


    def test_guest_user_cannot_remove(self):
        user = User.objects.get(username="user1")
        r = Reg.objects.first()
        c = Client()
        response = c.get(reverse('regs:remove', args=(r.id,)))
        self.assertEqual(r.students.count(), 1)


    def test_authenticated_user_can_remove(self):
        user = User.objects.get(username="user1")
        r = Reg.objects.first()
        c = Client()
        c.force_login(user)
        response = c.get(reverse('regs:remove', args=(r.id,)))
        self.assertEqual(r.students.count(), 0)
