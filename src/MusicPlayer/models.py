from django.db import models
from django.urls import reverse
from config import settings
from django.contrib.auth.models import User

class Song(models.Model):
    title= models.CharField(max_length=200)
    artist= models.CharField(max_length=200)
    image= models.ImageField(default=settings.STATIC_ROOT 
                             + 'imgs/user_default_img.avif')
    audio_file = models.FileField()
    genres = models.CharField(max_length=200, null=True, blank=True)
    listeners = models.ManyToManyField(User, blank=True)


    def __str__(self):
        return self.title
    
    

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(default=settings.STATIC_ROOT 
                              + 'imgs/user_default_img.avif')
    owner = models.ForeignKey(User, models.CASCADE)
    song = models.ManyToManyField(Song)

    def __str__(self) -> str:
        return self.title
