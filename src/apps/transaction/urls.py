from django.urls import path
from .views import *
urlpatterns = [
    path('search', SearchView.as_view(), name='transaction_search'),
    path('search/result', SearchUserView.as_view(), name='transaction_search_result'), 
]
