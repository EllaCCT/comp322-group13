from django.urls import path
from .views import *
from products.views import product_detail
from django.contrib.auth import views

urlpatterns = [
    path('', index, name='index'),
    path('product/', product, name='product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('signup/', register, name='signup'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/', login ,name='login')
]