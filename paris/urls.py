from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('room/<pk>', views.room, name='room'),

    path('create-room/', views.createRoom, name='create-room'), 
    path('update-room/<pk>', views.updateRoom, name='update-room'),
    path('delete/<pk>', views.deleteRoom, name='delete'),
    
    path('delete-room/<pk>', views.deleteMessage, name='delete-room'),
    path('delete-actvity/<pk>', views.deleteActivity, name='delete-actvity'),

    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),

    path('profile/<pk>', views.userProfile, name='user-profile'),


    path('edit-profile', views.editProfile, name='edit-profile'),


    path('more-section', views.moreSection, name='more-section'),

]