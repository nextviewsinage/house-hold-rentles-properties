from django.db import models


# Create your models here.


class feedback (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    feedback = models.TextField()    
       
    
    
   