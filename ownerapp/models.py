from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class rentals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_rentals')
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)
    rent_time = models.DateTimeField()
    phonenumber = models.BigIntegerField()


class category(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField(null=True)


class product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_products')
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    details = models.TextField(null=True)
    image = models.ImageField(upload_to="product_image")


class FinalOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_orders')
    total = models.BigIntegerField()
    gst = models.IntegerField()


class confirmorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirm_orders')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    final = models.ForeignKey(FinalOrder, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=40)
    total = models.IntegerField()
    subtotal = models.IntegerField()
