
from django.contrib import admin
from django.urls import path

from users import views
from users.views import index,shop
from products.views import product_detail
#from . import views

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('product/', product_detail, name='product_detail'),
    path('admin/', admin.site.urls),
]
