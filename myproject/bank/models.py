from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class Register(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='bank_register',  # Unique related_name
    )
    
    account_num = models.CharField(max_length=20, unique=True, blank=True)
    upi_id = models.CharField(max_length=50, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True,null=True)  # <-- Date field added
    profile_picture = models.ImageField(
        upload_to='static/profile/', blank=True, null=True
    ) 

    def generate_account_number(self):
        while True:
            acc = "ACC" + str(random.randint(10000000, 99999999))
            if not Register.objects.filter(account_num=acc).exists():
                return acc

    def save(self, *args, **kwargs):
        if not self.account_num:
            self.account_num = self.generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_num}"


# Signal to create Register automatically when a User is created
@receiver(post_save, sender=User)
def create_user_register(sender, instance, created, **kwargs):
    if created:
        Register.objects.create(user=instance)
