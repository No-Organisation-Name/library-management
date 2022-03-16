from django.shortcuts import render
from .models import Type
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ListTypeView(View):
    template_name = 'list_type.html'

    def get(self, request):
        obj = Type.objects.all()
        paginator = Paginator(obj, 5)
        page = request.GET.get('page')
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
        })
