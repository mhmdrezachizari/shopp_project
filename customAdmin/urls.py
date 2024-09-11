
from django.contrib import admin
from django.urls import path,include
from .views import LoginView , product_list , product_create , product_delete , product_update
app_name = 'customAdmin'
urlpatterns = [
  path('', LoginView.as_view(), name='auth-form'),
    path('products/', product_list, name='product_list'),
    path('products/create/',product_create, name='product_create'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
]
