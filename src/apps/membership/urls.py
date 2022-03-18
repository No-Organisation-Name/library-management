from django.urls import path
from .views import *

urlpatterns = [
    path('type', ListTypeView.as_view(), name='type_list'),
    path('member', ListMemberView.as_view(), name='member_list'),
    path('member/save', ListMemberView.as_view(), name='member_save'),
    path('type/save', ListTypeView.as_view(), name='type_save'),
    path('type/<int:id>/edit', EditTypeView.as_view(), name='type_edit'),
    path('type/<int:id>/update', EditTypeView.as_view(), name='type_update'),
    path('type/<int:id>/delete', DeleteTypeView.as_view(), name='type_delete'),
]
