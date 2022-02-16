from django.contrib import admin
from .models import Contributor
from .models import Category


class ContributorAdmin(admin.ModelAdmin):
    pass


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_at', 'update_at']


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Category, BookCategoryAdmin)
