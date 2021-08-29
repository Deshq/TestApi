from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class File(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255)  
    docfile = models.FileField(verbose_name='Docfile', upload_to=user_directory_path, max_length=100)
    daysOfvalidity = models.IntegerField(verbose_name='DaysOfvalidity', 
    default=30, editable=True, 
    validators=[
            MaxValueValidator(90),
            MinValueValidator(1)
        ])
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)