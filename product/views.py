from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Cart, CartItem, Discount
from django.utils import timezone
# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "product/index.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
class ProductDetailView(DetailView):
    model = Product
    template_name = "product/single.html"
    context_object_name = "product"



class CartView(View):
    @method_decorator(login_required)
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        total_amount = 0
        discount_amount = 0
        user = request.user
        for item in items:
            total_amount += item.product.price * item.quantity
        discount_code = request.GET.get('discount_code')
        if discount_code:
            try:
                discount = Discount.objects.get(user=user, discountCode=discount_code)
                discount_amount = discount.valueDecimal
                total_amount = total_amount - (total_amount * (discount_amount / 100))
                if total_amount < 0:
                    total_amount = 0
            except Discount.DoesNotExist:
                discount_amount = 0

        return render(request, 'product/cart_detail.html', {
            'cart': cart,
            'items': items,
            'total_amount': total_amount,
            'discount_amount': discount_amount,
        })
class AddToCartView(View):
    @method_decorator(login_required)
    def get(self, request, product_id):
        total_amount = 0
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += 1

        item.save()
        return redirect('product:cart_detail')

class RemoveFromCartView(View):
    @method_decorator(login_required)
    def get(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect('product:cart_detail')
