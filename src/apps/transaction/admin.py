from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'date_out', 'date_return')


class BorrowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Borrow, BorrowAdmin)
