from django.db import models


# Create your models here.
class transfer_record(models.Model):
    transfer_record_id = models.AutoField(primary_key=True)
    account_in_id = models.IntegerField()
    account_out_id = models.IntegerField()
    transfer_amount = models.IntegerField()
    transfer_date = models.DateField()

    def __str__(self):
        return self.transfer_record_id