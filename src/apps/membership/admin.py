from django.contrib import admin
from .models import Type


class TypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Type, TypeAdmin)
