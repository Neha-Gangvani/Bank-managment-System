from django.db import models
from django.contrib.auth.models import User


class Statement(models.Model):
    TYPE = (
        ('credit', 'Credit'),
        ('deduct', 'Deduct'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='statements'
    )
    bal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=10, choices=TYPE,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.bal}"
