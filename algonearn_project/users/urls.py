
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('auth/', views.RegisterView.as_view(), name='auth'),
]