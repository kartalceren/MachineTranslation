from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path, reverse_lazy

from . import views

app_name = 'site'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logged/', views.loggedinhome, name='loggedinhome'),
    path('password/', views.password, name='password'),
    path('password_reset/',
         auth_view.PasswordResetView.as_view(
             template_name='users/password_reset/password_reset.html',
             success_url=reverse_lazy('site:password_reset_done'),
             email_template_name='users/password_reset/password_reset_email.html',
             subject_template_name='users/password_reset/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset_done/',
         auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset/password_reset_sent.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',
         auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_form.html',
                                                    success_url=reverse_lazy('site:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_success.html'),
         name='password_reset_complete'),
    path('translateenglish/', views.translator_english, name='translatorEnglish'),
    path('translateturkish/', views.translator_turkish, name='translatorTurkish'),
    path('translate/', views.translate, name='translate')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
