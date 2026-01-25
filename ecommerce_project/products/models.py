from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # এই নিচের ফিল্ডগুলো কি আপনার ফাইলে আছে? না থাকলে যোগ করুন:
    storage = models.CharField(max_length=50, blank=True, null=True)
    ram = models.CharField(max_length=50, blank=True, null=True)

    # models.py এর Product ক্লাসের ভেতর যোগ করুন
def get_savings(self):
    if self.old_price:
        return self.old_price - self.price
    return 0

    def __str__(self):
        return self.name



