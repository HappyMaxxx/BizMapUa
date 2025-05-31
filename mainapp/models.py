from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    koatuu = models.CharField(max_length=100)
    img = models.ImageField(upload_to='regions/', blank=True, null=True)

    def __str__(self):
        return self.name


# class Businesse(models.Model):