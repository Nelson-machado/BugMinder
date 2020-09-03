from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('aboutPage', views.aboutPage, name='aboutPage'),
    path('search', views.search, name='search'),
    path('signup', views.signupAct, name='signupAct'),
    path('login', views.loginAct, name='loginAct'),
    path('logout', views.logoutAct, name='logoutAct'),
]