from django.shortcuts import render
from .models import Image, Category


def home(request):
    images = Image.objects.all()
    categories = Category.objects.all()
    context = {'images': images, 'categories': categories}
    return render(request, 'images/home.html', context)

