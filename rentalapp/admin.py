from django.contrib import admin
from .models import product


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'photo')
    search_fields = ('name',)
