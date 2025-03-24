from django.urls import path
from .views import *

from django.contrib.auth import views

urlpatterns = [
    path('', product_list, name='product'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]