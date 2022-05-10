from django.urls import path

from . import views

urlpatterns = [
    path('<usuario>/acoes/', views.index, name='index'),
    path('login/', views.login, name='login'),
]