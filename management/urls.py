from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('products/',ProductListView.as_view(),name='vendor_product_list',),
    path('products/<int:pk>',ProductUpdateView.as_view(), name='product_update'),
    path('products/add', AddProductView.as_view(), name='product_add'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrderListView.as_view(), name='vendor_order_list'),
    path('orders/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
]
