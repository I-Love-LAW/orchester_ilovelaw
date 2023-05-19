from django.db import models

class Pembayaran(models.Model):
    username = models.CharField(max_length=50)
    date = models.DateTimeField()
