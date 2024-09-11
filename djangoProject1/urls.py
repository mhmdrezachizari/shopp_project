
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',include('customAdmin.urls'),name = 'costumAdmin'),
    path('product/', include('product.urls'),name='product'),
    path('accounts/', include('accounts.urls') ,name='accounts'),
    path('superuser/',include('susercustom.urls'),name='superuser'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)