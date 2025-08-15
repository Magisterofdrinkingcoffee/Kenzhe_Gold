from django.contrib import admin
from .models import Brand, Type, Product, Order, OrderItem, BirthdayClient

admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BirthdayClient)
