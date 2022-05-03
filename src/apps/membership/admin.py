from django.contrib import admin
from .models import Type, Membership


class TypeAdmin(admin.ModelAdmin):
    pass

class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Type, TypeAdmin)
