from django.urls import path
from .views import *

urlpatterns = [
    path('products/',ProductListView.as_view(),name='vendor_product_list',),
    path('products/<int:pk>',ProductUpdateView.as_view(), name='product_update'),
    path('products/add', AddProductView.as_view(), name='product_add')
]
