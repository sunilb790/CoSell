from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from PIL import Image
from django.urls import reverse


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Premium = models.BooleanField(default=False)
    MobileNumber = models.CharField(max_length=10)

    class college_list(models.Model):
        COLLEGE_CHOICES = [
            ('IIITV', 'Indian Institute of Information Technology Vadodara (Gandhinagar Campus)'),
            ('IITB', 'Indian Institute of Technology Bombay'),
            ('IIITL', 'Indian Institute of Information Technology Lucknow'),
            ('IITK', 'Indian Institute of Technology Kanpur'),
            ('GEC', 'Government Engineering College,Gandhinagar'),
        ]
    college = models.CharField(
        max_length=5, choices=college_list.COLLEGE_CHOICES)

    def __str__(self):
        return self.user.username

    def getCollegeChoice(self):
        return self.college_list.COLLEGE_CHOICES


class Payment(models.Model):
    transection_id = models.CharField(max_length=30)
    Amount_paid = models.PositiveIntegerField()
    Date = models.DateTimeField(default=datetime.now)
    Student_Info = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.transection_id


class Product(models.Model):
    # Not Using default id provided by Django
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField(blank=False)  # Description is must
    Price = models.PositiveIntegerField()
    # Date once added cannot be changed
    DateTime = models.DateTimeField(default=timezone.now)
    SellerInfo = models.ForeignKey(Student, on_delete=models.CASCADE)
    Photo = models.ImageField(
        default='Balti.jpg', upload_to='ProductImages')
    payment = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product Name : {self.Name} and Its Id : {self.Id} '

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


class FAQ(models.Model):
    Id = models.AutoField(primary_key=True)
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    DateTime = models.DateTimeField(default=timezone.now)
    Query = models.TextField(max_length=200)
    Answer = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.UserName} | Query : {self.Query}'


class SellerBuyer(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_set")
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.seller} : {self.buyer} : {self.product}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='Resume_image.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
