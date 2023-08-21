from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Song
from .forms import RegisterForm, LoginForm


def index(request):
    print(request.user)
    paginator= Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,"MusicPlayer/index.html",context)

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'MusicPlayer/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully')
            login(request, user)
            return redirect('App:index')
        else:
            return render(request, 'MusicPlayer/register.html', {'form': form})
        
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'MusicPlayer/login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'You have signed in successfully')
                return redirect('App:index')

        messages.error(request, 'This user doesn\'t exist or data are invalid')
        return render(request, 'MusicPlayer/login.html', {'form': form})
    
def sign_out(request):
    logout(request)
    messages.error(request, 'You have been logged out')
    return redirect('App:index')