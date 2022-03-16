from django.urls import path
from .views import *

urlpatterns = [
    path('type', ListTypeView.as_view(), name='type_list'),
]
