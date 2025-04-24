from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('prueba/', views.prueba, name='prueba'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('api/message/<int:pk>/', views.delete_message_ws, name='delete-message-ws'),
    path('home_feed/', views.PostListView.as_view(), name='home_feed'),
    path('home_feed/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('home_feed/<int:pk>/dislike', views.Dislike.as_view(), name='dislike')
]