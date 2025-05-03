from django.db import models
from django.contrib.auth.models import User
from communities.models import Community, Tag  # ✅ Import Tag

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, through='Participation', related_name='events')
    tags = models.ManyToManyField(Tag, blank=True, related_name='events')  # ✅ Tag support

    def __str__(self):
        return self.title

class Participation(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'Going'),
        ('MAYBE', 'Maybe'),
        ('NOT_GOING', 'Not Going'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='GOING')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
