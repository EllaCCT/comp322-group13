from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #userIcon = models.ImageField(upload_to="image", blank=True, null=True)
  #description = models.TextField(max_length=1024, blank=True)
  email = models.EmailField(max_length=254, default="test@testmail.com")
  address = models.TextField(max_length=200, default="", blank=False,null=False)
  
  def __str__(self):
    return str(self.user)