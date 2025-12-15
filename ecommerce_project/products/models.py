from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=50, default="Unknown")  # ডিফল্ট মান
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # ডিফল্ট Category ID
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    slug = models.SlugField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    old_price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    release_date = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    display = models.CharField(max_length=100)
    camera = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    battery = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')


    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.title




