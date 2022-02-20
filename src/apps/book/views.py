from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Contributor, Category, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddContributorForm, AddCategoryForm,  AddBookForm, EditContributorForm
import datetime
from django.http import HttpResponse

class ContributorListView(View):
    template_name = 'contributor/contributor_list.html'
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


class ContributorEditView(View):
    template_name = 'contributor/contributor_edit.html'

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


class DeleteContributorView(View):
    def get(self, request, id):
        contributor = Contributor.objects.get(id=id)
        contributor.delete()
        return redirect(reverse('contributor_list'))


class CategoryListView(View):
    templates_name = 'category/category_list.html'

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

class CategoryEditView(View):
    templates_name = 'category/category_edit.html'
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


class DeleteCategoryView(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(reverse('category_list'))


class BookListView(View):
    template_name = 'book/book_list.html'

    def get(self, request):
        obj_list = Book.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        form = AddBookForm(request.POST)
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
        })

    def post(self, request):
        form = AddBookForm(request.POST, request.FILES)
        category = Category.objects.get(id=request.POST['category'])
        if form.is_valid():
            print("Valid Cuy")
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

class DeleteBookView(View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return redirect(reverse('book_list'))


def test(request):
    return render(request, 'contributor/test.html')
