from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    details = models.TextField(null=True)
    photo = models.ImageField(upload_to='product_image')
    quantity = models.IntegerField()