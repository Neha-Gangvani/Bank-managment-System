from django.db import models
from django.contrib.auth.models import User


#create Profile table
class Profile(models.Model):
    ROLE = (
        ('customer', 'Customer'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='accounts_profile' ,null=False # << unique name
    )
    role = models.CharField(max_length=50, choices=ROLE, default='customer')
    branch = models.ForeignKey('bank_system.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    bal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Message=models.CharField(max_length=500,blank=True)
    Response=models.CharField(max_length=500,blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"



