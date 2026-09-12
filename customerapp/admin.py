from django.contrib import admin
from .models import feedback


@admin.register(feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'feedback')
    search_fields = ('name', 'email', 'phone')
