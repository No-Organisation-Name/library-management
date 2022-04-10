from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from apps.transaction.models import Transaction
from apps.membership.forms import *
from apps.membership.models import *
from apps.book.models import Exemplar
from django.http import HttpResponse
from django.urls import reverse
import random
import string
import datetime
from datetime import timedelta

class SearchView(View):
    template_name = 'transaction/search.html'

    def get(self, request):
        form = SearchForm(request.POST)
        return render(request, self.template_name,{
            'form': form,
        })


class AdminSearchingBookView(View):
    template_name = 'transaction/search_book.html'

    def get(self, request, id):
        form = SearchBookForm(request.POST)
        return render(request, self.template_name,{
            'form': form,
            'id':id,
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


class AdminBookResultView(View):
    template_name='transaction/search_book_result.html'

    def post(self,request,id):
        form = SearchBookForm(request.POST)
        if form.is_valid():
            try:
                book = Exemplar.objects.get(barcode=str(form.cleaned_data['any_data']), status=True)
                form= SearchBookForm()
            except:
                book = None
                form= SearchBookForm()
            return render(request, self.template_name,{
                'form': form,
                'book': book,
                'id':id,
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
            membership.fine = Type.objects.get(name=form.cleaned_data['member_type']).fine
            membership.save()
            return redirect(reverse('transaction_search'))
        else:
            return HttpResponse(form.errors)
        

class DetailUserView(View):
    template_name = 'transaction/detail_user.html'

    def get(self, request,id):
        member = Membership.objects.get(id=id)
        loan_transactions = member.transactions.all()
        fines = [t.fine for t in loan_transactions.filter(status=True)]
        total_fine = sum(fines)
        if loan_transactions.filter(status=True).count() < member.member_type.amount_of_book and total_fine == 0:
            add_transaction = True
        else:
            add_transaction = False

        if loan_transactions.filter(status=True) and total_fine == 0:
            return_button = True
        else:
            return_button = False
        return render(request, self.template_name,{
            'member': member,
            'loan_transactions': loan_transactions.filter(status=True),
            'loan_history': loan_transactions.filter(status=False),
            'loan_fine': loan_transactions.filter(status=True).filter(fine__gt=0),
            'add':add_transaction,
            'return_button':return_button,
            'total_fine':total_fine,
            'id':id
        })


class AdminCheckoutBookView(View):

    def get(self,request, id, bcr):
        exmpl = Exemplar.objects.get(barcode=bcr)
        exmpl.status = False
        exmpl.save()
        member = Membership.objects.get(id=id)
        now = datetime.datetime.now()
        new_transaction = Transaction()
        new_transaction.user = member
        new_transaction.exemplar = Exemplar.objects.get(barcode=bcr)
        new_transaction.date_out = now
        new_transaction.date_return = now + timedelta(days=member.member_type.span_of_time)
        new_transaction.save()
        return redirect(reverse('transaction_detail_user', args=[f'{id}']))


class ReturnTransactionView(View):

    def get(self, request, id):
        member = Membership.objects.get(id=id)
        member_trans = member.transactions.filter(status=True)
        exemplars = Exemplar.objects.filter(transactions__user=member)
        for mt in member_trans:
            mt.status = False
            mt.save()
        for e in exemplars:
            e.status = True
            e.save()

        return redirect(reverse('transaction_detail_user', args=[f"{id}"]))
