#import django forms
from django import forms

class AddTypeOfMemberForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    span_of_time = forms.CharField(label='Span Of Time', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    fine = forms.CharField(label='Fine', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount_of_book = forms.CharField(label='Amount of Book', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cost = forms.CharField(label='Cost', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))