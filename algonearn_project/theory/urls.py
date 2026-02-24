from django.urls import path
from . import views

app_name = 'theory'  # пространство имен для ссылок

urlpatterns = [
    path('', views.theory_page, name='theory_page'),
]