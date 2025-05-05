from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')
    date_of_birth = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    postcode = models.CharField(max_length=20, blank=True)

    
    def __str__(self):
        return f'{self.user.username} Profile'
