from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .views import translator_english, TranslationHistoryView


def user_not_logged(user):
    return not user.is_authenticated


def redirect_authenticated_user(request):
    if request.user.is_authenticated:
        return redirect('site:loggedinhome')  # Change 'your_redirect_url' to the desired URL
    return True


app_name = 'site'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logged/', views.loggedinhome, name='loggedinhome'),
    path('password/', views.password, name='password'),
    path('password_reset/',
         user_passes_test(user_not_logged, login_url='site:loggedinhome')(auth_view.PasswordResetView.as_view(
             template_name='users/password_reset/password_reset.html',
             success_url=reverse_lazy('site:password_reset_done'),
             email_template_name='users/password_reset/password_reset_email.html',
             subject_template_name='users/password_reset/password_reset_subject.txt'
         )),
         name='password_reset'),
    path('password_reset_done/',
         user_passes_test(user_not_logged, login_url='site:home')(
             auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset/password_reset_sent.html')),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',
         user_passes_test(user_not_logged, login_url='site:home')(
             auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_form.html',
                                                        success_url=reverse_lazy('site:password_reset_complete'))),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         user_passes_test(user_not_logged, login_url='site:home')(auth_view.PasswordResetCompleteView.as_view(
             template_name='users/password_reset/password_reset_success.html')),
         name='password_reset_complete'),
    path('translateenglish/', views.translator_english, name='translatorEnglish'),
    path('translateturkish/', views.translator_turkish, name='translatorTurkish'),
    path('translate/', views.translate, name='translate'),
    path('translationhistory/', TranslationHistoryView.as_view(), name='translationHistory')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
