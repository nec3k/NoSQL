from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from Module1 import views

urlpatterns = [
    path('', views.downloader, name='downloader'),
    path('files/', views.file_manager, name='file_manager'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('login/', views.login_page, name='login_page'),
    path('password-change/', views.password_change, name='password_change'),
    path('logout/', views.logout_page, name='logout'),
    path('media/<str:path>', views.protected_serve, name='media_serve'),
]
