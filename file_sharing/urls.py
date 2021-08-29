from django.contrib import admin
from django.urls import path, include 
from file_sharing.views import *

app_name = 'file'

urlpatterns = [
    path('file/create/', FileCreateView.as_view()),  # as_view ???
    path('all/', FilesListView.as_view()),
    path('file/detail/<int:pk>/', FileDetailView.as_view()),
]
