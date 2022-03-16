from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=100)
    span_of_time = models.IntegerField()
    fine = models.CharField(max_length=15)
    amount_of_book = models.IntegerField()
    cost = models.CharField(max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'type'

