from django.urls import path

from . import views

urlpatterns = [
    path('friend/<int:pk>/', views.friend, name='friend'),
]
