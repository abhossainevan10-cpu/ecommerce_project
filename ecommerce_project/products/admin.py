from django.contrib import admin
from .models import Product, Category, Slider


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'storage', 'ram']
    list_filter = ['category', 'brand'] 
    search_fields = ['name', 'brand']
    list_editable = ['price']

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']