from django.urls import path
from .views import *

urlpatterns = [
    path('type', ListTypeView.as_view(), name='type_list'),
    path('member', ListMemberView.as_view(), name='member_list'),
    path('member/save', ListMemberView.as_view(), name='member_save'),
    path('member/<int:id>/edit', UpdateMemberView.as_view(), name='member_edit'),
    path('member/<int:id>/update', UpdateMemberView.as_view(), name='member_update'),
    path('member/<int:id>/delete', DeleteMemberView.as_view(), name='member_delete'),
    path('type/save', ListTypeView.as_view(), name='type_save'),
    path('type/<int:id>/edit', EditTypeView.as_view(), name='type_edit'),
    path('type/<int:id>/update', EditTypeView.as_view(), name='type_update'),
    path('type/<int:id>/delete', DeleteTypeView.as_view(), name='type_delete'),
]
