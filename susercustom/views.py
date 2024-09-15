from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User
from product.models import Product
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm
from product.models import Discount
from .forms import DiscountForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    next_page = "susercustom:user_approval_list"
    form_class = LoginForm

@user_passes_test(lambda u: u.is_superuser)
@login_required
def user_approval_list(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'susercustom/user_approval_list.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def approve_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect('/superuser/admin/users/')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('/superuser/admin/users/')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def product_approval_list(request):
    products = Product.objects.filter(is_active=False)
    return render(request, 'susercustom/product_approval_list.html', {'products': products})


@user_passes_test(lambda u: u.is_superuser)
@login_required
def approve_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = True
    product.save()
    return redirect('/superuser/admin/products')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('/superuser/admin/products')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def active_user(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount_code = form.cleaned_data['discountCode']
            user = form.cleaned_data['user']
            valueDecimal = form.cleaned_data['valueDecimal']
            Discount.objects.create(user=user, discountCode=discount_code , valueDecimal=valueDecimal)
            return redirect('/superuser/admin/verifyUser')

    users = User.objects.all()
    form = DiscountForm()
    context = {'users': users, 'form': form}
    return render(request, 'susercustom/verifyUser.html', context)
