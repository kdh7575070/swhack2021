from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('mbti/', views.mbti, name='mbti'),
    path('result/', views.result, name='result'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('mypage/',views.mypage,name='mypage'),
    path('edituser/',views.edituser,name='edituser'),
    path('updateuser/',views.updateuser,name='updateuser'),
]

