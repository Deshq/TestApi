from django.db.models import fields
from rest_framework import serializers
from file_sharing.models import File

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File 
        fields =  ('id','title','user')
        
class FileDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = File 
        fields = '__all__' # показываем что работаем со всеми полями
