from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
