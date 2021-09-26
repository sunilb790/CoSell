from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

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

class Product(models.Model):
    Id= models.AutoField(primary_key=True) #  Not Using default id provided by Django
    Name = models.CharField(max_length=100)
    Description = models.TextField(blank=False) #Description is must
    Price =  models.DecimalField(max_digits=10,decimal_places=2)
    DateTime=models.DateTimeField(default=timezone.now) #Date once added cannot be changed
    SellerInfo = models.ForeignKey(Student, on_delete=models.CASCADE)
    Photo = models.ImageField(default='NotsetDefaultPicture.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'Id is {self.Id} Name is {self.Name}'
