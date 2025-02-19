
from django.contrib import admin
from django.urls import path

from users import views
from users.views import index,product
from products.views import product_detail
#from . import views

urlpatterns = [
    path('', index, name='index'),
    path('product/', product, name='product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('admin/', admin.site.urls),
]
