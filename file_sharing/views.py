from django.shortcuts import render
from rest_framework import generics
from file_sharing.serializers import FileDetailSerializer, FileListSerializer
from file_sharing.models import File
from file_sharing.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

class FileCreateView(generics.CreateAPIView):
    serializer_class = FileDetailSerializer
    queryset = File.objects.all() 
    permission_classes = (IsAuthenticated, ) 


class FilesListView(generics.ListAPIView):
    serializer_class = FileListSerializer
    queryset = File.objects.all() # queryset - это для того, что бы указать какие записи брать с бд
    permission_classes = (IsAuthenticated, ) 
    
class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileDetailSerializer
    queryset = File.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly) # изменение только для того пользователя который и создал