from django.shortcuts import render, redirect
from .models import Image, Category
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from django.core.exceptions import BadRequest


@login_required(login_url='/login')
def home(request):
    images = Image.objects.all()
    categories = Category.objects.all()
    context = {'images': images, 'categories': categories}
    return render(request, 'images/home.html', context)


@login_required(login_url='/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            form.save()
            return redirect('/')
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload_image.html', {'form': form})


@login_required(login_url='/login')
def delete_image(request, pk):
    image = Image.objects.get(id=pk)
    if image.author == request.user:
        if request.method == 'POST':
            image.delete()
            return redirect('/')
        context = {'image': image}
        return render(request, 'images/delete_image.html', context)
    else:
        raise BadRequest("You do not have permission to see this site")