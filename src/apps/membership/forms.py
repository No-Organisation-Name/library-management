#import django forms
from random import choices
from django import forms
from .models import Type

class AddTypeOfMemberForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    span_of_time = forms.CharField(label='Span Of Time', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    fine = forms.CharField(label='Fine', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount_of_book = forms.CharField(label='Amount of Book', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cost = forms.CharField(label='Cost', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class AddMembershipForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Last Name'}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'username'}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder':'Password',}))
    password2 = forms.CharField(label='Confirm Password', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder':'Confirm Password',}))
    email = forms.CharField(required=False,label='Email', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'email@gmail.com'}))
    member_type = forms.ModelChoiceField(queryset=Type.objects.all(),label='Member Type', widget=forms.Select(attrs={
        'class': 'form-control'}))
    nik = forms.CharField(label='NIK', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'NIK'}))
    place_of_birth = forms.CharField(label='Place Of Birth', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Place Of Birth'}))
    date_of_birth = forms.CharField(label='Date of Birth', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#date_of_birth',
        'placeholder': 'Date of Entry',
        'id': 'date_of_entry',
        'placeholder': 'Date Of Birth'
    }))
    gender = forms.ChoiceField(label='Gender',choices=(
        ('Male', 'Male'),
        ("Female","Female")
    ),widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Gender'
    }))
    faith = forms.CharField(label='Faith', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Faith'}))
    married = forms.BooleanField(label='Married', required=False)
    job = forms.CharField(label='Job', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Job'}))
    phone_number = forms.CharField(label='Phone Number', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Phone Number'}))
    address = forms.CharField(label='Address', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Address'}))
    cost = forms.CharField(label='Cost', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'cost',
        'placeholder':'Rp. 0'}))