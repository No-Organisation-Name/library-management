from django.shortcuts import render, redirect
#import reverse 
from django.urls import reverse
from .models import Type, Membership, User
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddTypeOfMemberForm,AddMembershipForm, EditMembershipForm
from django.http import HttpResponse
import datetime
import random
import string
class ListTypeView(View):
    template_name = 'list_type.html'

    def get(self, request):
        obj = Type.objects.all()
        paginator = Paginator(obj, 5)
        page = request.GET.get('page')
        form = AddTypeOfMemberForm()
        try:
            type_of_members = paginator.page(page)
        except PageNotAnInteger:
            type_of_members = paginator.page(1)
        except EmptyPage:
            type_of_members = paginator.page(paginator.num_pages)
        return render(request, self.template_name,{
            'types':type_of_members.object_list,
            'type_of_member':type_of_members,
            'range':paginator.page_range,
            'page_now':type_of_members.number,
            'form':form,
        })

    def post(self, request):
        form = AddTypeOfMemberForm(request.POST)
        if form.is_valid():
            type_of_member = Type()
            type_of_member.name = form.cleaned_data['name']
            type_of_member.span_of_time = form.cleaned_data['span_of_time']
            type_of_member.fine = form.cleaned_data['fine']
            type_of_member.amount_of_book = form.cleaned_data['amount_of_book']
            if form.cleaned_data['cost'] == '':
                type_of_member.cost = 0
            else:
                type_of_member.cost = form.cleaned_data['cost']
            type_of_member.save()
        return redirect(reverse('type_list'))


class EditTypeView(View):
    template_name = 'type_edit.html'
    
    def get(self,request, id):
        obj = Type.objects.get(id=id)
        data = {
            'name':obj.name,
            'span_of_time':obj.span_of_time,
            'fine':obj.fine,
            'amount_of_book':obj.amount_of_book,
            'cost':obj.cost,
        }
        form_edit = AddTypeOfMemberForm(initial=data)
        return render(request, self.template_name, {'form_edit': form_edit, 'id':id})

    def post(self, request, id):
        obj = Type.objects.get(id=id)
        form = AddTypeOfMemberForm(request.POST)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.span_of_time = form.cleaned_data['span_of_time']
            obj.fine = form.cleaned_data['fine']
            obj.amount_of_book = form.cleaned_data['amount_of_book']
            if form.cleaned_data['cost'] == '':
                obj.cost = 0
            else:
                obj.cost = form.cleaned_data['cost']
            obj.save()
        return redirect(reverse('type_list'))

class DeleteTypeView(View):
    def get(self,request, id):
        obj = Type.objects.get(id=id)
        obj.delete()
        return redirect(reverse('type_list'))


class ListMemberView(View):
    template_name = 'members_list.html'

    def get(self, request):
        obj = Membership.objects.all()
        paginator = Paginator(obj, 5)
        page = request.GET.get('page')
        form =  AddMembershipForm()
        try:
            members = paginator.page(page)
        except PageNotAnInteger:
            members = paginator.page(1)
        except EmptyPage:
            members = paginator.page(paginator.num_pages)
        return render(request, self.template_name,{
            'members':members.object_list,
            'member':members,
            'range':paginator.page_range,
            'page_now':members.number,
            'form':form
        })

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
            membership.fine = Type.objects.get(id=form.cleaned_data['member_type']).fine
            membership.save()
            return redirect(reverse('member_list'))
        else:
            return HttpResponse(form.errors)

class UpdateMemberView(View):
    template_name = 'members_edit.html'

    def get(self, request,id):
        member= Membership.objects.get(id=id)
        data ={
            'first_name':member.user.first_name,
            'last_name':member.user.last_name,
            'username':member.user.username,
            'password':'',
            'email':member.user.email,
            'member_type':member.member_type,
            'nik':member.nik,
            'place_of_birth':member.place_of_birth,
            'date_of_birth':member.date_of_birth,
            'gender':member.gender,
            'faith':member.faith,
            'married':member.married,
            'job':member.job,
            'address':member.address,
            'phone_number':member.phone_number,
        }
        form = EditMembershipForm(initial=data)
        print(data['member_type'].fine)
        return render(request, self.template_name,{
            'form':form,
            'id':id
        })
    
    def post(self, request, id):
        form = EditMembershipForm(request.POST)
        if form.is_valid():
            member = Membership.objects.get(id=id)
            user = User.objects.get(id=member.user.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            if form.cleaned_data['password'] != '':
                user.set_password(form.cleaned_data['password'])
            user.save()
            member.member_type = form.cleaned_data['member_type']
            member.nik = form.cleaned_data['nik'].replace('_','').replace(' ','')            
            member.place_of_birth = form.cleaned_data['place_of_birth']
            member.date_of_birth = datetime.datetime.strptime(form.cleaned_data['date_of_birth'], "%Y-%m-%d")
            member.gender = form.cleaned_data['gender']
            member.faith = form.cleaned_data['faith']
            member.married = form.cleaned_data['married']
            member.job = form.cleaned_data['job']
            member.address = form.cleaned_data['address']
            member.phone_number = form.cleaned_data['phone_number'].replace('_','').replace(' ','')
            member.fine = Type.objects.get(name=form.cleaned_data['member_type']).fine
            member.save()
        else:
            return HttpResponse(form.errors)
        return redirect(reverse('member_list'))

class DeleteMemberView(View):
    def get(sel,request,id):
        member = Membership.objects.get(id=id)
        member.delete()
        return redirect(reverse('member_list'))