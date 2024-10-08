from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, VerifyCodeForm, LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from extensions.utils import send_otp
from .models import User, OtpCode
import random

# Create your views here.
class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            cd = form.cleaned_data
            phone_number = cd["phone_number"]
            send_otp(code, phone_number)
            OtpCode.objects.create(phone_number=phone_number, code=code)
            request.session["user_registration_info"] = {
                "phone_number": phone_number,
                "email": cd["email"],
                "about_me": cd["about_me"],
                "first_name": cd["first_name"],
                "last_name": cd["last_name"],
                "password": cd["password2"],
            }
            return redirect("accounts:verify")
        return render(request, self.template_name, {"form": form})


class UserVerifyView(View):
    form_class = VerifyCodeForm
    template_name = "accounts/verify.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user_session = request.session.get("user_registration_info")
        if not user_session:
            return redirect("accounts:register")  # Redirect if session data is not available

        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            code_instance = OtpCode.objects.filter(phone_number=user_session["phone_number"]).first()

            if code_instance and code == code_instance.code:
                user = User.objects.create(
                    phone_number=user_session["phone_number"],
                    email=user_session["email"],
                    about_me=user_session["about_me"],
                    first_name=user_session["first_name"],
                    last_name=user_session["last_name"],
                )
                user.set_password(user_session["password"])
                user.is_active = False
                user.save()
                code_instance.delete()
                redirect('/accounts/login')
                if user is not None:
                    login(request, user)
                    del request.session["user_registration_info"]
                    return redirect("product:list")

        return render(request, self.template_name, {"form": form})

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    next_page = "product:list"
    form_class = LoginForm

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:login")
