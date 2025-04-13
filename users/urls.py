from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('', index, name='index'),
    #path('product/', product, name='product'),
    #path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('signup/', register, name='signup'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/', login ,name='login')
]