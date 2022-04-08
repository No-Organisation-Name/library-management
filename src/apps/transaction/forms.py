#django import class form
from django import forms


class SearchForm(forms.Form):
    any_data = forms.CharField(max_length=45, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'NIK'}))
    