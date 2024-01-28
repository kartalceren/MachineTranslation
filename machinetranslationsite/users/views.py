from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.

def home(request):
    return render(request, 'users/home.html')


def login(request):
    return render(request, 'users/login.html')


def loggedinhome(request):
    return render(request, 'users/loggedinhome.html')


def logout(request):
    return render(request, 'users/logout.html')


def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, f'Your password was updated successfully.')
            return redirect(reverse('site:password'))
        else:
            messages.error(request, f'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form
    }

    return render(request, 'users/password.html', context)


def register(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Hi {username}, your account was created successfully. Please login to continue.')
            return redirect(reverse('site:home'))

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile was updated successfully.')
            return redirect(reverse('site:profile'))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'users/profile.html', context)
