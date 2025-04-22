from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', register, name='signup'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/', login ,name='login')
]