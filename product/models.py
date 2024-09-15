from datetime import timezone

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from accounts.models import User
class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    increadibleoffer = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def get_category(self):
        return ", ".join([cat.name for cat in self.category.all()])

class TopBanner(models.Model):
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FormSearchModel(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # expires_at = models.DateTimeField()
    discountCode = models.CharField(max_length=10,unique=True)
    valueDecimal = models.IntegerField(default=10)
    used = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.discountCode}"
