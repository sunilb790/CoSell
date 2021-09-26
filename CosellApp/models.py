from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Premium = models.BooleanField(default=False)
    MobileNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
