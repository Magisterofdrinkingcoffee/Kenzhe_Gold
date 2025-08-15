from django.contrib import admin
from .models import Brand, Type, Product, Order,OrderItem, BirthdayClient

admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BirthdayClient)



from django.contrib import admin
from .models import Brand, Type, Product, Order, OrderItem, BirthdayClient
from django.contrib.auth import get_user_model

admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BirthdayClient)

# --- ВРЕМЕННО: авто-создание суперпользователя ---
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="tuf",
        email="beka2007azimut@gmail.com",
        password="Riot_070507"
    )
