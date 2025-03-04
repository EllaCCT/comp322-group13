from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Member(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #userIcon = models.ImageField(upload_to="image", blank=True, null=True)
  #description = models.TextField(max_length=1024, blank=True)
  email = models.EmailField(max_length=254, default="")
  address = models.CharField(max_length=200, default="", blank=False,null=False)
  
  def __str__(self):
    return str(self.user)
  
  @receiver(post_save, sender=User)
  def _post_save_receiver(sender, instance, created, **kwargs):
    if created:
      Member.objects.create(user=instance)