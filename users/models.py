from django.db import models
from django.contrib.auth.models import User
from PIL import Image 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override save method of profile model to resize image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # to run

        img = Image.open(self.image.path) #import Image from PIL and open the image
        
        # Resizing and saving to 300x300 
        if img.height>300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)