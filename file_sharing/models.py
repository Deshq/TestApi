from datetime import datetime, date, time, timedelta, timezone 
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.forms import ValidationError

User = get_user_model()

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class FileManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset()\
            .filter(end_at__gt=datetime.now())\
            .filter(in_archive=False)

    def get_expired_files(self):
        return self.get_queryset()\
            .filter(end_at__gt=datetime.now() - timedelta(days=365))

    def delete_expired_files(self):
        File.objects.get_expired_files().delete()
        
class File(models.Model):
    
    title = models.CharField(verbose_name='Title', max_length=255)  
    slug = models.SlugField(verbose_name='Slug', unique=True)
    docfile = models.FileField(verbose_name='Docfile', upload_to=user_directory_path, max_length=100)
    created_at = models.DateField(verbose_name='Created_at',auto_now_add=True, db_index=True, editable=False)
    end_at = models.DateTimeField(verbose_name='End_at', default=datetime.now()+timedelta(days=30))
    countOfdownloads = models.IntegerField(verbose_name='CountOfdownloads', 
    default=0, editable=False)
    in_archive = models.BooleanField(verbose_name='In_archive', default=False)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    
    objects = FileManager()

    def save(self, *args, **kwargs):
        if self.end_at < datetime.now():
            raise ValidationError("The date cannot be in the past!")
        elif self.end_at > (datetime.now()+ timedelta(days=90)):
            raise ValidationError("Cant save file more 90 days")
        super(File, self).save(*args, **kwargs)

    class Meta:
        ordering=('-created_at',)
    
    
