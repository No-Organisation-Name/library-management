from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Contributor, Category, Book, Exemplar, BookShelf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from tablib import Dataset
from django.http import HttpResponse
import datetime
import mysql.connector as msql
from apps.book.models import ComeOutBook
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class ContributorListView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'contributor/contributor_list.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request):
        obj_list = Contributor.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        form = AddContributorForm(request.POST)
        try:
            contributor = paginator.page(page)
        except PageNotAnInteger:
            contributor = paginator.page(1)
        except EmptyPage:
            contributor = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'contributors': contributor.object_list,
            'contributor': contributor,
            'range': paginator.page_range,
            'page_now': contributor.number,
            'form': form,
        })

    def post(self, request):
        form = AddContributorForm(request.POST)
        if form.is_valid():
            contributor = Contributor()
            contributor.name = form.cleaned_data['name']
            contributor.description = form.cleaned_data['description']
            contributor.save()
        return redirect(reverse('contributor_list'))


class ContributorEditView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'contributor/contributor_edit.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        contributor = Contributor.objects.get(id=id)
        data = {
            'name': contributor.name,
            'description': contributor.description,
        }
        form_edit = EditContributorForm(initial=data)
        return render(request, self.template_name, {
            'form_edit': form_edit,
            'id': id,
        })

    def post(self, request, id):
        contributor = Contributor.objects.get(id=id)
        form = EditContributorForm(request.POST)
        if form.is_valid():
            contributor.name = form.cleaned_data['name']
            contributor.description = form.cleaned_data['description']
            contributor.save()
        return redirect(reverse('contributor_list'))


class DeleteContributorView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')
    
    def get(self, request, id):
        contributor = Contributor.objects.get(id=id)
        contributor.delete()
        return redirect(reverse('contributor_list'))


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    templates_name = 'category/category_list.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request):
        obj_list = Category.objects.all()
        paginator = Paginator(obj_list, 5)
        form = AddCategoryForm(request.POST)
        page = request.GET.get('page')
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        return render(request, self.templates_name, {
            'categories': categories.object_list,
            'category': categories,
            'range': paginator.page_range,
            'page_now': categories.number,
            'form': form,
        })

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category = Category()
            category.name = form.cleaned_data['name']
            category.save()
        return redirect(reverse('category_list'))

class CategoryEditView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    templates_name = 'category/category_edit.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        category = Category.objects.get(id=id)
        data = {
            'name': category.name,
        }
        form_edit = AddCategoryForm(initial=data)
        return render(request, self.templates_name, {
            'form_edit': form_edit,
            'id': id,
        })

    def post(self, request, id):
        category = Category.objects.get(id=id)
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.save()
        return redirect(reverse('category_list'))


class DeleteCategoryView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(reverse('category_list'))


class BookListView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/book_list.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')
    
    def get(self, request):
        obj_list = Book.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        form = AddBookForm(request.POST)
        form_exel = UploadExelForm()
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {
            'books': books.object_list,
            'book': books,
            'range': paginator.page_range,
            'page_now': books.number,
            'form': form,
            'form_exel': form_exel,
        })

    def post(self, request):
        form = AddBookForm(request.POST, request.FILES)
        category = Category.objects.get(id=request.POST['category'])
        if form.is_valid():
            book = Book()
            try:
                contributor = Contributor.objects.get(id=form.cleaned_data['contributor'])
                book.contributor = contributor
            except:
                pass
            book.category = category
            book.title = form.cleaned_data['title']
            book.description = form.cleaned_data['description']
            book.publisher = form.cleaned_data['publisher']
            book.publication_year = form.cleaned_data['publication_year']
            book.language = form.cleaned_data['language']
            book.isbn = form.cleaned_data['isbn']
            book.date_of_entry = datetime.datetime.strptime(form.cleaned_data['date_of_entry'], "%Y-%m-%d %H:%M")
            book.image = request.FILES['image']
            book.save()
        else:
            return HttpResponse(form.errors)
        return redirect(reverse('book_list'))


class UpdateBookView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/book_edit.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        book = Book.objects.get(id =id)
        data = {
            'title': book.title,
            'description': book.description,
            'publisher': book.publisher,
            'publication_year': book.publication_year,
            'language': book.language,
            'isbn': book.isbn,
            'date_of_entry': book.date_of_entry,
            'image': book.image,
            'contributor': book.contributor,
            'category': book.category,
        }
        form_edit = AddBookForm(initial=data)
        print(form_edit)
        return render(request, self.template_name, {
            'form_edit': form_edit,
            'id': id,
        })

    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = BookFormEdit(request.POST, request.FILES)
        category = Category.objects.get(id=request.POST['category'])
        if form.is_valid():
            try:
                contributor = Contributor.objects.get(id=form.cleaned_data['contributor'])
                book.contributor = contributor
            except:
                pass

            try:
                book.image = request.FILES['image']
            except:
                pass
            book.category = category
            book.title = form.cleaned_data['title']
            book.description = form.cleaned_data['description']
            book.publisher = form.cleaned_data['publisher']
            book.publication_year = form.cleaned_data['publication_year']
            book.language = form.cleaned_data['language']
            book.isbn = form.cleaned_data['isbn']
            book.date_of_entry = datetime.datetime.strptime(form.cleaned_data['date_of_entry'], "%Y-%m-%d %H:%M")
            book.save()
        else:
            return HttpResponse(form.errors)
        return redirect(reverse('book_list'))


class DeleteBookView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return redirect(reverse('book_list'))


class ImportBookView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def post(self, request):
        con = msql.connect(
            host='localhost', 
            database='lms_db',
            user='root', 
            password='apip'
            )
        cursor = con.cursor()
        form = UploadExelForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            new_data = request.FILES['upload_file']
            dataset = Dataset()
            import_data = dataset.load(new_data.read(), format='xls')
            for data in import_data:
                sql = ""f"INSERT INTO book (contributor_id, category_id, title, description, publisher, language, isbn, publication_year, create_at, update_at,date_of_entry, image) VALUES {data};"""
                cursor.execute(sql)
                con.commit()
            cursor.close()
            return redirect(reverse('book_list'))

        else:
            return HttpResponse(form.errors)


class ListExemplareView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/exemplar_list.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        form = AddStocksForm()
        this_book = Book.objects.get(id=id)
        obj = Exemplar.objects.filter(book_id=id)
        page = request.GET.get('page')
        paginator = Paginator(obj, 5)
        try:
            exemplars = paginator.page(page)
        except PageNotAnInteger:
            exemplars = paginator.page(1)
        except EmptyPage:
            exemplars = paginator.page(paginator.num_pages)
        try:
            bs = obj[0].bookshelf
        except:
            bs= 'None'
        return render(request, self.template_name,{
            'this_book':this_book,
            'exemplars':exemplars.object_list,
            'exemplar':exemplars,
            'range': paginator.page_range,
            'page_now': exemplars.number,
            'obj':obj,
            'bs':bs,
            'form':form,
            'id':id
        })

    def post(self, request, id):
        form = AddStocksForm(request.POST)
        if form.is_valid():
            exemplar = Exemplar()
            exemplar.book = Book.objects.get(id=id)
            exemplar.bookshelf = form.cleaned_data['bookshelf']
            exemplar.barcode = form.cleaned_data['barcode']
            exemplar.at_row = form.cleaned_data['at_row']
            exemplar.save()
        return redirect(reverse('exemplar_list', kwargs={'id': id}))

class UpdateExemplarView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/exemplar_edit.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id, exm):
        exemplar = Exemplar.objects.get(id=exm)
        form = AddStocksForm(initial={
            'bookshelf': exemplar.bookshelf,
            'barcode': exemplar.barcode,
            'at_row': exemplar.at_row,
        })
        return render(request, self.template_name, {
            'form': form,
            'id': id,
        })

    def post(self, request, id, exm):
        exemplar = Exemplar.objects.get(id=exm)
        form = AddStocksForm(request.POST)
        if form.is_valid():
            exemplar.bookshelf = form.cleaned_data['bookshelf']
            exemplar.barcode = form.cleaned_data['barcode']
            exemplar.at_row = form.cleaned_data['at_row']
            exemplar.save()
        return redirect(reverse('exemplar_list', kwargs={'id': id}))


class DeleteExemplarView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id, exm):
        exemplar = Exemplar.objects.get(id=exm)
        exemplar.delete()
        return redirect(reverse('exemplar_list', kwargs={'id': id}))


class ListBookComeOut(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/come_out_book.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')
    
    def get(self, request):
        obj = ComeOutBook.objects.all()
        print(obj)
        return render(request, self.template_name,{
            'obj':obj
        })

class AddBookCameOutView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/add_come_out_book.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request):
        form = AddComeOutBookForm()
        return render(request, self.template_name,{
            'form':form
        })

    def post(self, request):
        form = AddComeOutBookForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['exemplar'])
            print(form.cleaned_data['exemplar'].id)
            print(type(form.cleaned_data['exemplar']))
            come_out_book = ComeOutBook()
            come_out_book.exemplar = form.cleaned_data['exemplar']
            exemplar = Exemplar.objects.get(id=form.cleaned_data['exemplar'].id)
            exemplar.status = False
            exemplar.save()
            come_out_book.date_of_came_out = form.cleaned_data['date_of_came_out']
            come_out_book.description = form.cleaned_data['description']
            come_out_book.save()
            return redirect(reverse('come_out_list'))
        else:
            return HttpResponse(form.errors)


class EditComeOutBookView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    template_name = 'book/edit_come_out_book.html'
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        come_out_book = ComeOutBook.objects.get(id=id)
        data = {
            'exemplar': come_out_book.exemplar,
            'date_of_came_out': come_out_book.date_of_came_out,
            'description': come_out_book.description,
        }
        form = EditComeOutBookForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id,
        })

    def post(self, request, id):
        form = EditComeOutBookForm(request.POST)
        if form.is_valid():
            obj = ComeOutBook.objects.get(id=id)
            obj.exemplar = form.cleaned_data['exemplar']
            obj.date_of_came_out = form.cleaned_data['date_of_came_out']
            obj.description = form.cleaned_data['description']
            obj.exemplar.status = False
            obj.exemplar.save()
            obj.save()
            return redirect(reverse('come_out_list'))
        else:
            return HttpResponse(form.errors)

class DeleteComeOutBookView(LoginRequiredMixin, PermissionRequiredMixin ,View):
    login_url = '/login'
    permission_required = ('transaction.add_transaction')

    def get(self, request, id):
        obj = ComeOutBook.objects.get(id=id)
        obj.exemplar.status=True
        obj.exemplar.save()
        obj.delete()
        return redirect(reverse('come_out_list'))


    
class BookshelfView(View):
    template_name = 'book/list_bookshelf.html'
    login_url = '/login'

    def get(self, request):
        obj_list = BookShelf.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        form = BookShelfForm(request.POST)
        try:
            bookshelf = paginator.page(page)
        except PageNotAnInteger:
            bookshelf = paginator.page(1)
        except EmptyPage:
            bookshelf = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {
            'bookshelfs': bookshelf.object_list,
            'bookshelf': bookshelf,
            'range': paginator.page_range,
            'page_now':bookshelf.number,
            'form': form,
        })
    
    def post(self, request):
        form = BookShelfForm(request.POST)
        if form.is_valid():
            bookshelf = BookShelf()
            bookshelf.name = form.cleaned_data['name']
            bookshelf.number = form.cleaned_data['number']
            bookshelf.row = form.cleaned_data['row']
            bookshelf.save()
        return redirect(reverse('bookshelf_list'))