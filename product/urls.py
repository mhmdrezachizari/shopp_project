from django.urls import path,include
from .views import ProductListView ,ProductDetailView ,CartView, AddToCartView, RemoveFromCartView
app_name = 'product'
urlpatterns = [
    path('',ProductListView.as_view(),name='list'),
   path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]
