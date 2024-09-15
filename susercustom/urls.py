from django.urls import path
from .views import user_approval_list, approve_user, product_approval_list, approve_product , LoginView , delete_product,delete_user,active_user
app_name = 'susercustom'
urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('admin/users/', user_approval_list, name='user_approval_list'),
    path('admin/users/approve/<int:pk>/', approve_user, name='approve_user'),
    path('admin/users/delete/<int:pk>/', delete_user, name='delete_user'),
    path('admin/verifyUser/' , active_user , name='active_user'),# مسیرهای تأیید محصولات
    path('admin/products/', product_approval_list, name='product_approval_list'),
    path('admin/products/approve/<int:pk>/', approve_product, name='approve_product'),
    path('admin/products/delete/<int:pk>/', delete_product, name='delete_product'),
]
