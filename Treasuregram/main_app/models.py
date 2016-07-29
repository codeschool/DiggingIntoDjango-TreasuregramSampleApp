from django.db import models
from django.contrib.auth.models import User

def get_image_path(instance, filename):
    return '/'.join(['treasure_images', str(instance.name), filename])


class Treasure(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    image = models.ImageField(upload_to='treasure_images', default='media/default.png')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
