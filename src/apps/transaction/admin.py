from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('exemplar','user', 'date_out', 'date_return')


admin.site.register(Transaction, TransactionAdmin)
