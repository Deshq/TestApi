from datetime import datetime
from django.db.models.aggregates import Avg, Count, Sum
from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from file_sharing import serializers
from file_sharing.serializers import FileDetailSerializer, FileGetUrlSerializer, FileListSerializer
from file_sharing.models import File
from file_sharing.permissions import IsOwnerOrReadOnly, IsSuperUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import F
from rest_framework.filters import SearchFilter


# Create your views here.

class FileCreateView(generics.CreateAPIView):
    """File creation"""
    
    serializer_class = FileDetailSerializer
    queryset = File.objects.all() 
    permission_classes = (IsAuthenticated,) 

class FilesListView(generics.ListAPIView):
    """Displaying a list of files, filtering by id/title"""

    serializer_class = FileListSerializer
    queryset = File.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']
    permission_classes = (IsAuthenticated, ) 
    
class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Editing/deleting files if owner"""

    serializer_class = FileDetailSerializer
    queryset = File.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly) 

class FileGetAPIView(generics.RetrieveAPIView):
    """Getting a link to download a file"""

    serializer_class = FileGetUrlSerializer
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format=None): 

        qs = File.objects.filter(id = pk)\
            .filter(end_at__gt=datetime.now())                   
        qs.update(countOfdownloads=F('countOfdownloads') + 1)

        serializer = FileGetUrlSerializer(qs, many=True, context= {'request': request})
            
        if serializer.data:
            return Response({ 'status' : True, 'message' : 
                'File url', 'file' : serializer.data})     

        raise NotFound(detail="Error 404, page not found", code=404)

class StatisticsUserProfileView(generics.ListAPIView):

    serializer_class = FileListSerializer
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_top10_files(self, request, *args, **kwargs):

        qs = File.objects.all()\
            .filter(user_id=request.user.id)\
            .order_by('-countOfdownloads')\
            .filter(countOfdownloads__gt=0)[:10]

        serializer = FileListSerializer(qs, many=True, context= {'request': request})
        
        if serializer.data:
            return Response({'Top 10 downloads file in profile ': serializer.data})

        raise NotFound(detail="Error 404, page not found", code=404)

    def get(self, request, *args, **kwargs):
        return self.get_top10_files(request, *args, **kwargs)
    
           
class AdminDataView(generics.ListAPIView):
    """Returns a queryset as a serialized list"""

    queryset = File._base_manager.all()
    permission_classes = (IsSuperUser, )

    def get_queryset(self):
        # add complex lookup here
        queryset = self.queryset
        return queryset

class StatisticsView(AdminDataView):
    """Overwriting the get method to 
    serve different content"""

    def summarize(self, request, *args, **kwargs):

        qs = self.filter_queryset(self.get_queryset())\
            .aggregate(Sum('countOfdownloads'))
        qs2 = self.filter_queryset(self.get_queryset())\
            .aggregate(Count('id'))
        
        stats = {'File statistics': {'Sum file downloads': qs,
         'Count upload files' : qs2}}
        return Response(stats)

    def get(self, request, *args, **kwargs):
        return self.summarize(request, *args, **kwargs)

class StatisticsProfileView(AdminDataView):
    """Overwriting the get method to 
    serve different content"""

    def get_top10_profiles(self, request, *args, **kwargs):

        qs = File.objects.all().values('user_id')\
            .annotate(sum_downloads=Sum('countOfdownloads'))\
            .order_by('-sum_downloads')\
            .filter(sum_downloads__gt=0)[:10]

        stats = {'Top 10 profiles by downloads':qs}
        return Response(stats)

    def get(self, request, *args, **kwargs):
        return self.get_top10_profiles(request, *args, **kwargs)
