from django import forms


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
