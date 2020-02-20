from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title

    #We use reverse function to get the URL to a particular route, and not redirect function
    # redirect returned the page but reverse return the string of URL and views handles the rest
    # We need to use getabsoluteUrl method for django to find a location to a specific post
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
class StoreCoke(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})