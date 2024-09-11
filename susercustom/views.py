from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User
from product.models import Product
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    next_page = "susercustom:user_approval_list"
    form_class = LoginForm

# فقط سوپریوزرها بتوانند دسترسی داشته باشند
@user_passes_test(lambda u: u.is_superuser)
@login_required
def user_approval_list(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'susercustom/user_approval_list.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def approve_user(request, pk):
    # کاربر را پیدا می‌کنیم
    user = get_object_or_404(User, pk=pk)
    user.is_active = True  # کاربر را تأیید می‌کنیم
    user.save()
    return redirect('/superuser/admin/users/')  # بازگشت به لیست کاربران تایید نشده


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_user(request, pk):
    # کاربر را پیدا می‌کنیم
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('superuser/admin/users/')  # بازگشت به لیست کاربران تایید نشده
@user_passes_test(lambda u: u.is_superuser)
@login_required
def product_approval_list(request):
    # محصولات تایید نشده را فیلتر می‌کنیم
    products = Product.objects.filter(is_active=False)
    return render(request, 'susercustom/product_approval_list.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def approve_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = True
    product.save()
    return redirect('/superuser/admin/products')  # بازگشت به لیست محصولات تایید نشده
@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('/superuser/admin/products')  # بازگشت به لیست محصولات تایید نشده
