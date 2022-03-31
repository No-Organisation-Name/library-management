from django.urls import path
from .views import *

urlpatterns = [
    path('contributor/', ContributorListView.as_view(), name='contributor_list'),
    path('contributor/save', ContributorListView.as_view(), name='contributor_save'),
    path('contributor/edit/<int:id>', ContributorEditView.as_view(), name='contributor_edit'),
    path('contributor/update/<int:id>', ContributorEditView.as_view(), name='contributor_update'),
    path('contributor/<int:id>/delete', DeleteContributorView.as_view(), name='contributor_delete'),

    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/save', CategoryListView.as_view(), name='category_save'),
    path('category/edit/<int:id>', CategoryEditView.as_view(), name='category_edit'),
    path('category/update/<int:id>', CategoryEditView.as_view(), name='category_update'),
    path('category/<int:id>/delete', DeleteCategoryView.as_view(), name='category_delete'),


    path('', BookListView.as_view(), name='book_list'),
    path('save', BookListView.as_view(), name='book_save'),
    path('<int:id>/edit', UpdateBookView.as_view(), name='book_edit'),
    path('<int:id>/update', UpdateBookView.as_view(), name='book_update'),
    path('<int:id>/delete', DeleteBookView.as_view(), name='book_delete'),
    path('import_book', ImportBookView.as_view(), name='book_import'),
    
    
    path('<int:id>/exemplar', ListExemplareView.as_view(), name='exemplar_list'),
    path('<int:id>/exemplar/save', ListExemplareView.as_view(), name='exemplar_save'),
    path('<int:id>/exemplar/<int:exm>/edit', UpdateExemplarView.as_view(), name='exemplar_edit'),
    path('<int:id>/exemplar/<int:exm>/update', UpdateExemplarView.as_view(), name='exemplar_update'),
    path('<int:id>/exemplar/<int:exm>/delete', DeleteExemplarView.as_view(), name='exemplar_delete'),
]
