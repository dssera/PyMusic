from django.urls import path

from . import views


app_name = "App"

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),

    path('music/', views.index, name='index'),
    path('music/<str:username>/', views.personal_music_view, name='personal_music'),
]
