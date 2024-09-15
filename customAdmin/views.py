from django.shortcuts import render
from django.contrib.auth import views as auth_views
from accounts import forms
from accounts.forms import LoginForm
from .forms import ProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    next_page = "product:list"
    form_class = LoginForm
@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'customAdmin/product_list.html', {'products': products})

# ایجاد محصول جدید
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.is_active = False
            product.save()
            form.save_m2m()
            return redirect('/admin/products/')
    else:
        form = ProductForm()
    return render(request, 'customAdmin/product_form.html', {'form': form})

# ویرایش محصول
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.is_active = False
            form.save()
            return redirect('/admin/products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'customAdmin/product_form.html', {'form': form})

# حذف محصول
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('/admin/products')
    return render(request, 'customAdmin/product_confirm_delete.html', {'product': product})
