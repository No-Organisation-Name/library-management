from django.urls import path
from .views import *

urlpatterns = [
    path('type', ListTypeView.as_view(), name='type_list'),
    path('type/save', ListTypeView.as_view(), name='type_save'),
    path('type/<int:id>/delete', DeleteTypeView.as_view(), name='type_delete'),
]
