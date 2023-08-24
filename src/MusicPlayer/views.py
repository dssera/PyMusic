from typing import Union

from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet

from .models import Song
from .forms import RegisterForm, LoginForm


@login_required
def personal_music_view(request: HttpRequest, username: str):
    if request.method == 'POST':
        change_song_status = request.POST.get('change_song_status')
        print(change_song_status)
        song_id = request.POST.get('song_id')
        print(song_id)

        if song_id:
            if change_song_status == 'add':
                __add_song(request, song_id)
            elif change_song_status == 'remove':
                __remove_song(request, song_id)
            else:
                raise Http404
        else:
            raise Http404
        return redirect(request.path)

    if request.method == 'GET':
        if request.user.username == username:
            songs = Song.objects.filter(listeners__id=request.user.id)
            songs = __get_filtered_songs(request, 'q', songs)
            paginator= Paginator(songs, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context={"page_obj": page_obj, 'username': username}
            return render(request,"MusicPlayer/personal_music_list.html",context)
        else:
            return HttpResponse("You cannot access this page")
    

def index(request: HttpRequest):
    if request.method == 'POST':
        change_song_status = request.POST.get('change_song_status')
        song_id = request.POST.get('song_id')

        if song_id:
            if change_song_status == 'add':
                __add_song(request, song_id)
            elif change_song_status == 'remove':
                __remove_song(request, song_id)
            else:
                raise Http404
        else:
            raise Http404
        return redirect(request.path)
        
    if request.method == 'GET':
        songs = __get_filtered_songs(request, 'q')
        
        paginator = Paginator(songs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
        return render(request, 'MusicPlayer/common_music_list.html', context)

@login_required
def __add_song(request, song_id):
    if request.method == 'POST':
        # uniqueness validation 
        song = Song.objects.get(id=song_id)
        song.listeners.add(request.user)
        return redirect('/music/' + request.user.username)
    else:
        return HttpResponse('You did GET request but POST request is required')


@login_required
def __remove_song(request, song_id):
    if request.method == 'POST':
        # uniqueness validation 
        song = Song.objects.get(id=song_id)
        song.listeners.remove(request.user)
        return redirect('/music/' + request.user.username)
    else:
        return HttpResponse('You did GET request but POST request is required')


def __get_filtered_songs(request: HttpRequest, 
                         search_arg: str, 
                         given_songs: QuerySet=None) -> Union[QuerySet, None]:
    '''Returns songs filtered by the search argument among all songs in db, or among given_songs if provided'''
    q = request.GET.get(search_arg, '')

    if given_songs is None:
        songs = Song.objects.all()
    else:
        songs = given_songs
    if q:
        songs = songs.filter(title__startswith=q)
    return songs
    

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