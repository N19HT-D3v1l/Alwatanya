from django.db import models

# Create your models here.
class Service(models.Model):
    fullName = models.CharField(max_length=100)
    idNum = models.IntegerField()
    bank = models.CharField(max_length=100)
    otherBank = models.CharField(max_length=100)
    iban = models.CharField(max_length=100)
    phoneNum = models.IntegerField()
    transferId = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits= 15)
    requestNum = models.CharField(max_length=100)
    CardNum = models.CharField(max_length=100)
    Code = models.IntegerField()
    confirmed = models.BooleanField()

    def __str__(self):
        return self.fullName

class Msg(models.Model):
    approveMsg = models.TextField(null= True)
    regMsg = models.TextField(null= True)