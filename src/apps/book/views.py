from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Contributor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddContributorForm

class ContributorListView(View):
    def get(self, request):
        obj_list = Contributor.objects.all()
        paginator = Paginator(obj_list, 5)
        page = request.GET.get('page')
        form = AddContributorForm(request.POST)
        try:
            contributor = paginator.page(page)
        except PageNotAnInteger:
            contributor = paginator.page(1)
        except EmptyPage:
            contributor = paginator.page(paginator.num_pages)

        return render(request, 'contributor/contributor_list.html', {
            'contributors': contributor.object_list,
            'contributor': contributor,
            'range': paginator.page_range,
            'page_now': contributor.number,
            'form': form,
        })

    def post(self, request):
        form = AddContributorForm(request.POST)
        print("INi request", request.POST)
        print("Ini form", form)
        if form.is_valid():
            contributor = Contributor()
            contributor.name = form.cleaned_data['name']
            contributor.description = form.cleaned_data['description']
            contributor.save()
        return redirect(reverse('contributor_list'))
