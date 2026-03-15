from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('', views.practice_page, name='practice_page'),
    path('test/', views.test_page, name='test_page'),
]