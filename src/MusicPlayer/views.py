from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Song
from .forms import RegisterForm, LoginForm

# @login_required
# def add_song_view(request, song_id):
#     if request.method == 'POST':
#         # uniqueness validation 
#         song = Song.objects.get(id=song_id)
#         song.listeners.add(request.user)
#         return redirect(request.path)
#     else:
#         return HttpResponse('You did GET request but POST request is required')

@login_required
def personal_music_view(request, username, song_id=None):
    if request.method == 'GET':
        if request.user.username == username:
            paginator= Paginator(Song.objects.all(), 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context={"page_obj": page_obj, 'username': username}
            return render(request,"MusicPlayer/music_list.html",context)
        else:
            return HttpResponse("You cannot access this page")
    
    if request.method == 'POST':
        # uniqueness validation
        if song_id is None:
            return HttpResponse('Я должен был кидать пост запрос с \
                                аргументом song_id но я хз как правильно это сделать ')
        print(request.POST.get('song_id'))
        song = Song.objects.get(id=request.POST.get('song_id'))
        song.listeners.add(request.user)
        return redirect(request.path)


def index(request: HttpRequest):
    return render(request, 'MusicPlayer/index.html')




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