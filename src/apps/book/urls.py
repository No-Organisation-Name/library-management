from django.urls import path
from .views import ContributorListView

urlpatterns = [
    path('contributor/', ContributorListView.as_view(), name='contributor_list'),
]
