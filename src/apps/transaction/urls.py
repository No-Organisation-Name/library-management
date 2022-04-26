from django.urls import path
from .views import *
urlpatterns = [
    path('search/user', SearchView.as_view(), name='transaction_search_user'),
    path('user/result', SearchUserView.as_view(), name='transaction_search_result'), 
    path('create/user', CreateUserView.as_view(), name='transaction_add_new_user'), 
    path('<int:id>/user', DetailUserView.as_view(), name='transaction_detail_user'),
    path('<int:id>/user/add', AddTransactionView.as_view(), name='add_transaction'),
    path('<int:id>/user/detail_transaction', DetailTransactionView.as_view(), name='detail_transactions'),
    path('<int:id>/user/search/book', AdminSearchingBookView.as_view(), name='admin_searching_book'),
    path('<int:id>/user/book/result', AdminBookResultView.as_view(), name='admin_searching_book_result'),
    path('<int:id>/user/<str:bcr>/book/checkout', AdminCheckoutBookView.as_view(), name='book_checkout'),
    path('<int:id>/user/return', ReturnTransactionView.as_view(), name='return_transaction'),
]
