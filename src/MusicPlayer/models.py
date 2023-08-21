from django.db import models
from config import settings
from django.contrib.auth.models import User

class Song(models.Model):
    title= models.CharField(max_length=200)
    artist= models.CharField(max_length=200)
    image= models.ImageField(default=settings.STATIC_ROOT 
                             + 'imgs/user_default_img.avif')
    audio_file = models.FileField()
    genres = models.CharField(max_length=200, null=True, blank=True)
    # audio_link = models.CharField(max_length=200,blank=True,null=True)
    # duration=models.CharField(max_length=20)
    # paginate_by = 2

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
