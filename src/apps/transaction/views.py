from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from apps.membership.forms import *
from apps.membership.models import *
from django.http import HttpResponse
from django.urls import reverse
import random
import string

class SearchView(View):
    template_name = 'transaction/search.html'

    def get(self, request):
        form = SearchForm(request.POST)
        return render(request, self.template_name,{
            'form': form,
        })



class SearchUserView(View):
    template_name='transaction/search_result.html'

    def post(self,request):
        member_form = AddMembershipForm(request.POST)
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                member = Membership.objects.get(nik=form.cleaned_data['any_data'])
                form= SearchForm()
            except:
                member = None
                form= SearchForm()
            return render(request, self.template_name,{
                'form': form,
                'member': member,
                'member_form': member_form,
            })
        return HttpResponse(form.errors)

class CreateUserView(View):

    def post(self, request):
        form = AddMembershipForm(request.POST)
        print(request.POST['date_of_birth'])
        if form.is_valid():
            print('valid')
            letters = string.ascii_letters
            user = User()
            user.username = form.cleaned_data['first_name'].lower()
            user.password = ''.join(random.choice(letters) for i in range(10))
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            try:
                user.email = form.cleaned_data['email']
            except:
                pass
            user.save()
            membership = Membership()
            membership.user = user
            membership.member_type = form.cleaned_data['member_type']
            membership.nik = form.cleaned_data['nik']
            membership.place_of_birth = form.cleaned_data['place_of_birth']
            membership.date_of_birth = form.cleaned_data['date_of_birth']
            membership.gender = form.cleaned_data['gender']
            membership.address = form.cleaned_data['address']
            membership.faith = form.cleaned_data['faith']
            membership.married = form.cleaned_data['married']
            membership.job = form.cleaned_data['job']
            membership.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data['cost'] == '':
                membership.cost = 0
            else:
                membership.cost = form.cleaned_data['cost'].replace('.','')
            membership.save()
            return redirect(reverse('transaction_search'))
        else:
            return HttpResponse(form.errors)
        

class DetailUserView(View):
    template_name = 'transaction/detail_user.html'

    def get(self, request,id):
        member = Membership.objects.get(id=id)
        loan_transactions = member.transactions.all()
        return render(request, self.template_name,{
            'member': member,
            'loan_transactions': loan_transactions
        })