from django.contrib import admin
from .models import feedback, Wishlist, ProductReview, CustomerProfile, OrderStatus


@admin.register(feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'feedback')
    search_fields = ('name', 'email', 'phone')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_on')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_on',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'created_at')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'pincode')
    search_fields = ('user__username', 'phone', 'city')


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'updated_at')
    search_fields = ('order__id',)
    list_filter = ('status',)
    list_editable = ('status',)
