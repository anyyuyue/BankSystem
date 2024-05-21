from django.db import models


# Create your models here.
class CreditCard(models.Model):
    account_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=6)

    def __str__(self):
        return self.account_id

