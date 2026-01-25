# products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # এখানে 'title' থাকলে সেটি মুছে 'name' লিখে দিন
        fields = ['id', 'name', 'brand', 'price', 'image', 'storage', 'ram']