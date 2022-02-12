from django.urls import path
from .views import ContributorListView, ContributorEditView, DeleteContributorView

urlpatterns = [
    path('contributor/', ContributorListView.as_view(), name='contributor_list'),
    path('contributor/save', ContributorListView.as_view(), name='contributor_save'),
    path('contributor/edit/<int:id>', ContributorEditView.as_view(), name='contributor_edit'),
    path('contributor/update/<int:id>', ContributorEditView.as_view(), name='contributor_update'),
    path('contributor/delete/<int:id>', DeleteContributorView.as_view(), name='contributor_delete'),
]
