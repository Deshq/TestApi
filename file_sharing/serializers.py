from django.db.models import fields
from django.http import request
from rest_framework import serializers
from file_sharing.models import File
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ( "id", "username", "first_name", 'last_name', 'email', 'is_superuser')

class FileListSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = File 
        fields =  ('id','title','user','countOfdownloads', 'created_at', 'end_at')

class FileGetUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id',
            'docfile')

    def get_file_url(self, obj):
        request = self.context.get('request')
        file_url = obj.fingerprint.url
        return request.build_absolute_uri(file_url)

class FileDetailSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = File 
        fields = '__all__'
    
    def validate_title(self, value):
        title = value
        qs = File.objects.filter(title__iexact=title)
        if qs.exists():
            raise serializers.ValidationError("This title already exists")          
        return title 


