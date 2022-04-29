from turtle import update
from xml.parsers.expat import model
from django.db import models
from apps.membership.models import Membership
from apps.book.models import *

class Transaction(models.Model):
    user = models.ForeignKey(Membership, related_name='transactions', on_delete=models.CASCADE)
    date_out = models.DateTimeField()
    date_return = models.DateTimeField()
    fine = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.id}"

    class Meta:
        db_table = 'transactions'


class Borrow(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='borrows', on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, related_name='borrows', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transaction}--{self.exemplar}"

    class Meta:
        db_table = 'borrows'
