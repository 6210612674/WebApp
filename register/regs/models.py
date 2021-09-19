from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Reg(models.Model):
    
    SEMESTER = (('1', '1'), ('2','2'))

    class Status(models.IntegerChoices):
        Open = 1
        Close = 2

    course_status = models.IntegerField(choices = Status.choices)
    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=128)
    course_semester = models.CharField(max_length=200, choices = SEMESTER)
    course_quota = models.IntegerField()
    students = models.ManyToManyField(User, blank=True, related_name ="user_student") 

    def __str__(self):
        if self.course_quota-self.students.all().count() == 0:
            return f"{self.course_code} {self.course_name} {self.course_semester}/{datetime.date.today().year+543}  [Quota : FULL ]"
        return f"{self.course_code} {self.course_name} {self.course_semester}/{datetime.date.today().year+543}  [Quota : {self.course_quota-self.students.all().count()} ]"
