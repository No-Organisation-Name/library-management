from django.urls import path
from .views import *
urlpatterns = [
    path('search', SearchView.as_view(), name='transaction_search'),
    path('search/result', SearchUserView.as_view(), name='transaction_search_result'), 
    path('search/result/new', CreateUserView.as_view(), name='add_new_user'), 
    path('<int:id>/user', DetailUserView.as_view(), name='detail_user')
]
