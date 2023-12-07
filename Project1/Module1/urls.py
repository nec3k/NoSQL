from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from Project1.settings import EMAIL_HOST_USER
from Module1 import views

urlpatterns = [
    path('', views.downloader, name='downloader'),
    path('files/', views.file_manager, name='file_manager'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('login/', views.login_page, name='login_page'),
    path('password-change/', views.password_change, name='password_change'),
    path('logout/', views.logout_page, name='logout'),
    path('media/<str:path>', views.protected_serve, name='media_serve'),
    path('api/files/', views.api_files, name="api_files"),
    path('api/my_requests/', views.api_my_requests, name="api_my_requests"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html", from_email=EMAIL_HOST_USER),name='password_reset',),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done',),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name='password_reset_confirm',),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_complete.html",title='Obnova hesla proběhla úspěšně'),name='password_reset_complete',),
]
