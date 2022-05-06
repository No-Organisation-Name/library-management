from django.contrib import admin
from .models import Contributor, Category, Book, BookShelf ,Exemplar, ComeOutBook


class ContributorAdmin(admin.ModelAdmin):
    pass


class ExemplarAdmin(admin.ModelAdmin):
    pass


class BookShelfAdmin(admin.ModelAdmin):
    pass

class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_at', 'update_at']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'publisher', 'language', 'isbn' , 'publication_year', 'date_of_entry', 'image']


class ComeOutBookAdmin(admin.ModelAdmin):
    pass



admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Category, BookCategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Exemplar, ExemplarAdmin)
admin.site.register(BookShelf, BookShelfAdmin)
admin.site.register(ComeOutBook, ComeOutBookAdmin)
