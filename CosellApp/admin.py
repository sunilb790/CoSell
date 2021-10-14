from django.contrib import admin
from .models import Student, Payment, Product, FAQ, SellerBuyer,Profile

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(FAQ)
admin.site.register(SellerBuyer)
admin.site.register(Profile)