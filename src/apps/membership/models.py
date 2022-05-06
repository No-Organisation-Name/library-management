from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=100)
    span_of_time = models.IntegerField()
    fine = models.CharField(max_length=15)
    amount_of_book = models.IntegerField()
    cost = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'type'


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership')
    member_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='membership')
    nik =models.CharField(max_length=16)
    place_of_birth = models.CharField(max_length=25)
    date_of_birth = models.DateField()
    gender=models.CharField(max_length=12)
    address= models.CharField(max_length=150)
    faith = models.CharField(max_length=45)
    married = models.BooleanField(default=False)
    job = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=25)
    cost = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'membership'
