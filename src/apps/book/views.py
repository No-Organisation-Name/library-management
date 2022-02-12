from django.shortcuts import render
from django.views import View
from .models import Contributor
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ContributorListView(View):
    def get(self, request):
        obj_list = Contributor.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        try:
            contributor = paginator.page(page)
        except PageNotAnInteger:
            contributor = paginator.page(1)
        except EmptyPage:
            contributor = paginator.page(paginator.num_pages)

        print("page saat ini: ", contributor.number)
        print(paginator.page_range)
        return render(request, 'contributor/contributor_list.html', {
            'contributors': contributor.object_list,
            'contributor': contributor,
            'range': paginator.page_range,
            'page_now': contributor.number,
        })
