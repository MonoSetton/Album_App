from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=75, null=False, blank=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=False, blank=False)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, )

    def __str__(self):
        return self.name

