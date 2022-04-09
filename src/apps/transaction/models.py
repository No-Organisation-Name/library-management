from xml.parsers.expat import model
from django.db import models
from apps.membership.models import Membership
from apps.book.models import *

class Transaction(models.Model):
    user = models.ForeignKey(Membership, related_name='transactions', on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, related_name='transactions', on_delete=models.CASCADE)
    date_out = models.DateTimeField()
    date_return = models.DateTimeField()
    fine = models.IntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.exemplar.book.title

    class Meta:
        db_table = 'transactions'