from django.shortcuts import render
from .models import Image, Category
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def home(request):
    images = Image.objects.all()
    categories = Category.objects.all()
    context = {'images': images, 'categories': categories}
    return render(request, 'images/home.html', context)

