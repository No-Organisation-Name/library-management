"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import  handler403
from django.conf.urls.static import static
from apps.membership.views import LoginView, ReauthenticateView, LogoutView
from apps.transaction.views import *
from apps.book.views import *
from suka_suka.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('apps.book.urls')),
    path('membership/', include('apps.membership.urls')),
    path('transaction/', include('apps.transaction.urls')),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login/process', LoginView.as_view(), name='login_process'),
    path('reauthenticate', ReauthenticateView.as_view(), name='reauthenticate'),
    path('<str:username>', UserDashboardView.as_view(), name='user_dashboard'),
    path('<str:username>/search', UserSearchingBookView.as_view(), name='user_searchng_book'),
    path('<str:username>/book/result', UserBookResultView.as_view(), name='search_result_book'),
    path('<str:username>/book/<str:title>', UserBookDetailView.as_view(), name='user_exemplar_list'),
    path('suka_suka/', include('suka_suka.urls')),
    
]
handler403 = 'apps.membership.views.custom_error_403'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)