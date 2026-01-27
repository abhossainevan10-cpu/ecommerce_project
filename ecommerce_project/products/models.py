from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) 
    icon = models.ImageField(upload_to='cat_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
   
    storage = models.CharField(max_length=255, blank=True, null=True, help_text="স্পেস দিয়ে লিখুন: 128GB 256GB 512GB")
    ram = models.CharField(max_length=255, blank=True, null=True, help_text="স্পেস দিয়ে লিখুন: 8GB 12GB 16GB")
    color = models.CharField(max_length=255, blank=True, null=True, help_text="স্পেস দিয়ে লিখুন: Silver Black Orange")
    region = models.CharField(max_length=255, blank=True, null=True, help_text="স্পেস দিয়ে লিখুন: USA JP Global")
    
   
    stock_status = models.CharField(max_length=50, default="In Stock")
    warranty_info = models.CharField(max_length=200, default="1 Year Official Warranty Support")
    description = models.TextField(blank=True, null=True)

    def get_savings(self):
        if self.old_price:
            return self.old_price - self.price
        return 0

    def __str__(self):
        cat_name = self.category.name if self.category else "No Category"
        return f"{self.name} ({cat_name})"

class Slider(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='sliders/')
    
    def __str__(self):
        return self.title or f"Slider {self.id}"
