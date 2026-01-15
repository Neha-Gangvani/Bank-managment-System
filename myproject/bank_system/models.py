from django.db import models


# Branch table
class Branch(models.Model):
    name = models.CharField(max_length=100)  # Name of the branch
    city= models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name