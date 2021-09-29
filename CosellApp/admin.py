from django.contrib import admin
from .models import Student, Payment, Product, FAQ

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(FAQ)