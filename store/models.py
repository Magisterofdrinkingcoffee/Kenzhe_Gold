from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=100)
    price_per_gram = models.DecimalField(max_digits=100 , decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for product in self.product_set.all():
            product.save()  
    def __str__(self):
        return self.name
class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand , on_delete=models.CASCADE)
    type = models.ForeignKey(Type , on_delete= models.CASCADE)
    weight_in_grams = models.DecimalField(max_digits=10 , decimal_places=2)
    calculated_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null = True)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(blank=True, null=True)


    def save(self , *args, **kwargs):
        self.calculated_price = self.weight_in_grams * self.brand.price_per_gram
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default='Имя не указано')
    phone_number = models.CharField(max_length=20, default='0000000000')
    payment_method = models.CharField(max_length=50, choices=[
    ('cash', 'Наличные'),
    ('transfer', 'Перевод'),
    ], default='cash')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2)



class BirthdayClient(models.Model):
    full_name = models.CharField("ФИО",max_length=100)
    instagram_username = models.CharField("Instagram Username",max_length=100)
    phone_number = models.CharField("Номер WhatsApp", max_length=20, blank=True, null=True)
    birthday = models.DateField("Дата рождения")


    def __str__(self):
        return f"{self.full_name} ({self.instagram_username})"