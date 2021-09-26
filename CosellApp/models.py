from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Premium = models.BooleanField(default=False)
    MobileNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    transection_id = models.CharField(max_length=30)
    Amount_paid = models.PositiveIntegerField()
    Date = models.DateTimeField(default=datetime.now)
    Student_Info = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.transection_id
