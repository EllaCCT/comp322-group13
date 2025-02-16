from django.urls import path, re_path
from Backend.views.user.account.views import register, login, getInfo

urlpatterns = [
  path('register/', register, name='user_account_register'),
  re_path('login/', login),
  re_path('getinfo/', getInfo)
]