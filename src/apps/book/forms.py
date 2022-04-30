from cProfile import label
from django import forms
from .models import Contributor, Category, BookShelf, Exemplar, ComeOutBook


class AddContributorForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))


class EditContributorForm(forms.Form):
    id = forms.HiddenInput()
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))


class AddCategoryForm(forms.Form):

    id = forms.HiddenInput()
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name'
    }))


class AddBookForm(forms.Form):
    id = forms.HiddenInput()
    contributor = forms.ModelChoiceField(label='Contributor', queryset=Contributor.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Contributor'
    }), required=False)
    category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Category'
    }))
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))
    publisher = forms.CharField(label='Publisher', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Publisher'
    }))
    language = forms.CharField(label='Language', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Language'
    }))
    isbn = forms.CharField(label='ISBN', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ISBN',
        'data-inputmask': "'mask': '999-99-999-9999-9'",
        'data-mask': ''
    }))
    publication_year = forms.CharField(label='Publication Year', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'placeholder': 'Publication Year',
        'data-target': '#publication_year',
        'id': 'publication_year'
    }))
    date_of_entry = forms.CharField(label='Date of Entry', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#date_of_entry',
        'placeholder': 'Date of Entry',
        'id': 'date_of_entry'
    }))
    image = forms.ImageField(label='Image')

class AddCategoryForm(forms.Form):

    id = forms.HiddenInput()
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name'
    }))


class BookFormEdit(forms.Form):
    id = forms.HiddenInput()
    contributor = forms.ModelChoiceField(label='Contributor', queryset=Contributor.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Contributor'
    }), required=False)
    category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Category'
    }))
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))
    publisher = forms.CharField(label='Publisher', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Publisher'
    }))
    language = forms.CharField(label='Language', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Language'
    }))
    isbn = forms.CharField(label='ISBN', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ISBN',
        'data-inputmask': "'mask': '999-99-999-9999-9'",
        'data-mask': ''
    }))
    publication_year = forms.CharField(label='Publication Year', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'placeholder': 'Publication Year',
        'data-target': '#publication_year',
        'id': 'publication_year'
    }))
    date_of_entry = forms.CharField(label='Date of Entry', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#date_of_entry',
        'placeholder': 'Date of Entry',
        'id': 'date_of_entry'
    }))
    image = forms.ImageField(label='Image', required=False)

class UploadExelForm(forms.Form):
    upload_file = forms.FileField(label='Upload File')


class AddStocksForm(forms.Form):
    barcode = forms.CharField(label='Barcode', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Barcode'
        }))
    
    bookshelf = forms.ModelChoiceField(label='Book Shelf', queryset=BookShelf.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Category'
    }))

    at_row = forms.CharField(label='At Row', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'At Row'
        }))


class AddComeOutBookForm(forms.Form):
    id = forms.HiddenInput()
    exemplar = forms.ModelChoiceField(label='Exemplar', queryset=Exemplar.objects.filter(status=True), widget=forms.Select(attrs={
        'class': 'form-control'}))
    date_of_came_out = forms.CharField(label='Date of Come Out', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#date_of_came_out',
        'placeholder': 'Date of Come Out',
        'id': 'date_of_came_out'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))


class EditComeOutBookForm(forms.Form):
    id = forms.HiddenInput()
    exemplar = forms.ModelChoiceField(label='Exemplar',queryset=Exemplar.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'}))
    date_of_came_out = forms.CharField(label='Date of Come Out', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#date_of_came_out',
        'placeholder': 'Date of Come Out',
        'id': 'date_of_came_out'
    }))
    description = forms.CharField(label='Description', max_length=50, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description'
    }))