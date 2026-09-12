from django.contrib import admin
from .models import rentals, category, product, FinalOrder, confirmorder


@admin.register(rentals)
class RentalsAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phonenumber', 'rent_time', 'user')
    search_fields = ('name', 'email', 'phonenumber')
    list_filter = ('rent_time',)


@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    search_fields = ('name',)


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'user', 'image')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(FinalOrder)
class FinalOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'gst')
    search_fields = ('user__username',)


@admin.register(confirmorder)
class ConfirmOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'address', 'total', 'subtotal', 'final')
    search_fields = ('user__username', 'address')
