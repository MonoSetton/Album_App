from django.forms import ModelForm
from django import forms
from .models import Image, Category, Comment


class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'image', 'category']

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']