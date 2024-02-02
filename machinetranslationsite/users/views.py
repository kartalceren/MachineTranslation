from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from transformers import MarianMTModel, MarianTokenizer

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TranslationFormEnglish, TranslationFormTurkish


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/logged')
    return render(request, 'users/home.html')


def login(request):
    return render(request, 'users/login.html')


@login_required
def loggedinhome(request):
    return render(request, 'users/loggedinhome.html')


@login_required
def translate(request):
    return render(request, 'users/translation/translate_landing.html')


def logout(request):
    return render(request, 'users/logout.html')


@login_required
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
    if request.user.is_authenticated:
        return HttpResponseRedirect('/logged')
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


def translate_english(text, source_lang, target_lang):
    model_name = f'Helsinki-NLP/opus-tatoeba-en-tr'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)

    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return translated_text


@login_required
def translator_english(request):
    if request.method == 'POST':
        form = TranslationFormEnglish(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            source_lang = form.cleaned_data['source_language']
            target_lang = form.cleaned_data['target_language']

            translated_text = translate_english(text, source_lang, target_lang)
            return render(request, 'users/translation/english_translator.html',
                          {'form': form, 'translated_text': translated_text})
    else:
        form = TranslationFormEnglish()

    return render(request, 'users/translation/english_translator.html', {'form': form})


def translate_turkish(text, source_lang, target_lang):
    model_name = f'Helsinki-NLP/opus-mt-tr-en'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)

    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return translated_text


@login_required
def translator_turkish(request):
    if request.method == 'POST':
        form = TranslationFormTurkish(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            source_lang = form.cleaned_data['source_language']
            target_lang = form.cleaned_data['target_language']

            translated_text = translate_turkish(text, source_lang, target_lang)
            return render(request, 'users/translation/turkish_translator.html',
                          {'form': form, 'translated_text': translated_text})
    else:
        form = TranslationFormTurkish()

    return render(request, 'users/translation/turkish_translator.html', {'form': form})
