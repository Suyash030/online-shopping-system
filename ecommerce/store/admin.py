from django.contrib import admin
from .models import Category, Product, Order, OrderItem
from .models import Review
admin.site.register(Review)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)