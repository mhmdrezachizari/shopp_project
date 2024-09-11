from django.urls import path
from .views import UserRegistrationView, UserVerifyView ,LoginView,LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
