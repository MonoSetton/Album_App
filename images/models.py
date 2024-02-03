from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=75, null=False, blank=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=False, blank=False)
    likes = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField(max_length=350)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
