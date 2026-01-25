from django.contrib import admin
from .models import Product # আপনার মডেলটি ইমপোর্ট করুন

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # অ্যাডমিন প্যানেলে কোন কোন কলাম দেখাবে তা এখানে বলে দিন
    list_display = ['name', 'brand', 'price', 'storage', 'ram']
    list_filter = ['brand'] # সাইডবারে ফিল্টার অপশন যোগ করবে
    search_fields = ['name', 'brand'] # সার্চ বক্স যোগ করবে