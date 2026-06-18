from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    list_select_related = ('created_by',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    search_fields = ('name', 'description', 'created_by__username')
