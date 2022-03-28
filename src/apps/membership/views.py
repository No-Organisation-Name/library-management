from django.shortcuts import render, redirect
#import reverse 
from django.urls import reverse
from .models import Type
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddTypeOfMemberForm
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


class DeleteTypeView(View):
    def get(self,request, id):
        obj = Type.objects.get(id=id)
        obj.delete()
        return redirect(reverse('type_list'))
