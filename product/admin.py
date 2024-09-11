from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from product.models import Category ,Product

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)