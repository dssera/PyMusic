from django.urls import path

from . import views


app_name = "App"

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),


    # path('music/add_song/<int:song_id>', views.add_song_view, name='add_song'),
    path('music/<str:username>/', views.personal_music_view, name='personal_music'),
    path('music/<str:username>/<int:song_id>', views.personal_music_view, name='personal_music'),
    # path('add_song/<int:song_id', views.add_song_view, name='add_song'),
    path('', views.index, name='index')
]
