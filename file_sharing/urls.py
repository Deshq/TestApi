from django.contrib import admin
from django.urls import path, include 
from file_sharing.views import *

app_name = 'file'

urlpatterns = [
    path('file/create/', FileCreateView.as_view()), 
    path('file/all/', FilesListView.as_view()),
    path('file/detail/<int:pk>/', FileDetailView.as_view()),
    
    path('user/statistics/profile/', StatisticsUserProfileView.as_view()),


  
    path('file/get/<int:pk>/', FileGetAPIView.as_view()), # для получения ссылки скачивания 

    path('admin/statistics/', StatisticsView.as_view()),
    path('admin/statistics/profile/', StatisticsProfileView.as_view()),

]
