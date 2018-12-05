from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    """Customer reviews"""
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='deleted user', related_name='reviews')
    title = models.CharField(max_length=40)
    content = models.TextField()
    image = models.ImageField(upload_to='reviews/photos', blank=True, null=True)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} {self.title} {self.time_created}"