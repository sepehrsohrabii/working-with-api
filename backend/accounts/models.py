from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(blank=True, max_length=20, verbose_name='phone')
    class Meta:
        verbose_name = 'user info'
        verbose_name_plural = 'users info'
    def __str__(self):
        return self.user.username
