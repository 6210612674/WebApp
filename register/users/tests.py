from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import *
from regs.models import Reg


# Create your tests here.


class UserViewTestCase(TestCase):

    def setUp(self):
        reg = Reg.objects.create(course_status='1', course_code='CN210', course_name='Architecture', course_semester='2', course_quota='5')
        user = User.objects.create(username='user1', password = make_password('1234'), email='user@example.com')


    def test_index_view_with_authentication(self):
        user = User.objects.get(username='user1')
        c = Client()
        c.force_login(user)
        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)


    def test_index_view_without_authentication(self):
        user = User.objects.get(username='user1')
        c = Client()
        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 302)


    def test_login_view_successful(self):
        user = User.objects.get(username='user1')
        c = Client()
        c.force_login(user)
        response = c.post(reverse('users:login'), {'username': 'user1', 'password': '1234'})
        self.assertEqual(response.status_code, 302)


    def test_login_view_with_authentication(self):
        user = User.objects.get(username='user1')
        c = Client()
        c.force_login(user)
        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)


    def test_login_view_without_authentication(self):
        user = User.objects.get(username='user1')
        c = Client()
        response = c.post(reverse('users:login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)


    def test_logout_view(self):
        user = User.objects.get(username='user1')
        c = Client()
        response = c.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)


    def test_result_view(self):
        user = User.objects.get(username='user1')
        c = Client()
        response = c.get(reverse('users:results'))
        self.assertEqual(response.status_code, 200)

    def test_result_view_inreg(self):
        user = User.objects.get(username='user1')
        reg = Reg.objects.get(course_code='CN210')
        reg.students.add(user)
        reg.save()
        c = Client()
        c.force_login(user)
        response = c.get(reverse('users:results'))
        self.assertEqual(user, reg.students.first())
