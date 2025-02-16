from django.urls import path, include

urlpatterns = [
  path('',include('Backend.urls.user.account.urls')),
]