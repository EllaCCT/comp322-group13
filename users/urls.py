from django.urls import path
from .views import index, product
from products.views import product_detail
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('product/', product, name='product'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    #path('signup/', views.SignUpView.as_view(), name='signup'),
]