from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from . import settings
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls')),
    path('', RedirectView.as_view(url='app1')),
    path('accounts/', include('allauth.urls')),

    path('password/change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/change-password.html'),
         name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/change-password-done.html'),
         name='password_change_done'),

    path('reset/password/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password-reset.html'),
         name='password_reset'),
    path('reset/password/send/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password-reset-message.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password-reset-key.html'),
         name='password_reset_confirm'),
    path('reset/password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password-reset-key-done.html'),
         name='password_reset_complete'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
