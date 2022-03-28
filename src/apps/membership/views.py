from django.shortcuts import render, redirect
#import reverse 
from django.urls import reverse
from .models import Type, Membership, User
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddTypeOfMemberForm,AddMembershipForm
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
        if form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                user = User()
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
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
                membership.cost = form.cleaned_data['cost'].replace('.','')
                print("cost:",form.cleaned_data['cost'].replace('.',''))
                membership.save()
            else:
                pass
        return redirect(reverse('member_list'))