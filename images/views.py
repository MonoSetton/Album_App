from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Image, Category, Comment
from .filters import ImageFilter
from .forms import ImageUploadForm, CommentForm


@login_required(login_url='/login')
def home(request):
    images = Image.objects.all()
    categories = Category.objects.all()

    search_filter = ImageFilter(request.GET, queryset=images)
    images = search_filter.qs

    form = CommentForm

    context = {'images': images, 'categories': categories, 'search_filter': search_filter, 'form': form}
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
            return redirect('/profile')
        context = {'image': image}
        return render(request, 'images/delete_image.html', context)
    else:
        raise BadRequest("You do not have permission to see this site")


def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.image = Image.objects.get(id=pk)
            form.save()

            # Return a JSON response with the new comment data
            data = {'body': comment.body, 'author': comment.author.username}
            return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Invalid form submission'})


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('/')

