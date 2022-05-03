from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from apps.transaction.models import Transaction
from apps.membership.forms import *
from apps.membership.models import *
from apps.book.models import Exemplar
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import string
import datetime
from datetime import timedelta, date

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
        try:
            member = Membership.objects.get(id=id)
            loan_transactions = member.transactions.filter(status=True)
            total_fine = loan_transactions[0].fine
            total_exemplar = loan_transactions[0].borrows.all().count()
        except:
            total_fine = 0
            total_exemplar = 0

        print(total_fine)
        print(total_exemplar)
        if  total_exemplar < member.member_type.amount_of_book and total_fine <= 0 and loan_transactions.count() < 1:
            add_transaction = True
        else:
            add_transaction = False

        if loan_transactions.count() == 1 and  total_fine <= 0 and total_exemplar > 0:
            return_button = True
        else:
            return_button = False

        if loan_transactions:
            print("table")
        else:
            print("no table")

        print(f'total fine : {total_fine}')
        print(f'total exemplar : {total_exemplar}')
        print(f"add transaction : {add_transaction}")
        print(f"return button : {return_button}")
        print(f"Loan Transaction {loan_transactions}")
        print(f"Loan History {loan_transactions.filter(status=False)}")
        print(f"Loan With Fine : {loan_transactions.filter(status=True, fine__gt=0)}")
        print(f"id : {id}")
        return render(request, self.template_name,{
            'member': member,
            'loan_transactions': member.transactions.filter(status=True),
            'loan_history': member.transactions.filter(status=False),
            'loan_fine': member.transactions.filter(status=True).filter(fine__gt=0),
            'add':add_transaction,
            'return_button':return_button,
            'total_fine':total_fine,
            'id':id,
            'total_exemplar':total_exemplar
        })

    
class AddTransactionView(View):

    def get(self, request, id):
        member = Membership.objects.get(id=id)
        tomorrow = date.today() + timedelta(days=member.member_type.span_of_time)
        midnight = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())
        transaction = Transaction()
        transaction.user = member
        transaction.date_out = datetime.datetime.now()
        transaction.date_return = midnight
        transaction.fine = 0
        transaction.save()
        return redirect('transaction_detail_user',id=id)

class DetailTransactionView(View):
    
    template_name = 'transaction/detail_transaction.html'

    def get(self, request,id):
        exemplar = Membership.objects.get(id=id).transactions.filter(status=True)[0].borrows.all()
        if exemplar.count() < Membership.objects.get(id=id).member_type.amount_of_book:
            add_exemplar = True
        else:
            add_exemplar = False
        return render(request, self.template_name,{
            'id':id,
            'exemplar':exemplar,
            'add_exemplar':add_exemplar,
        })


from apps.transaction.models import Borrow
class AdminCheckoutBookView(View):

    def get(self,request, id, bcr):
        transaction_id = Membership.objects.get(id=id).transactions.filter(status=True)[0]
        new_exemplar = Borrow()
        new_exemplar.transaction = transaction_id
        new_exemplar.exemplar = Exemplar.objects.get(barcode=bcr)
        new_exemplar.exemplar.status = False
        new_exemplar.exemplar.save()
        new_exemplar.save()
        return redirect(reverse('transaction_detail_user', args=[f'{id}']))


class ReturnTransactionView(View):

    def get(self, request, id, id_transaction):
        transaction = Transaction.objects.get(id=id_transaction)
        exemplars = transaction.borrows.all()
        transaction.status = False
        transaction.save()
        for e in exemplars:
            e.exemplar.status = True
            e.exemplar.save()

        return redirect(reverse('transaction_detail_user', args=[f"{id}"]))



class ActiveTransactionView(View):
    template_name = 'transaction/active_transaction.html'

    def get(self,request):
        obj = Transaction.objects.filter(status=True)
        paginator = Paginator(obj, 5)
        page = request.GET.get('page')
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)
        return render(request, self.template_name,{
            'transactions':transactions.object_list,
            'transaction':transactions,
            'range':paginator.page_range,
            'page_now':transactions.number,
        })