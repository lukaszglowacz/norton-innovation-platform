from .models import Comment, Post
from django import forms
from django.utils.text import slugify
from PIL import Image
import io


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'image')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'btn, btn-sm'}),
        }
        labels = {
            'body': 'Comment',
            'image': 'Upload image'
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            img = Image.open(image)
            max_size = (800, 800)  # Max size (width, height)
            img.thumbnail(max_size, Image.LANCZOS)
            img_io = io.BytesIO()
            img_format = img.format if img.format else 'JPEG'
            img.save(img_io, format=img_format, quality=60)
            img_io.seek(0)  # Reset file pointer to the beginning
            image.name = 'resized_' + image.name  # Change the image filename
            # Update the image file to the resized image
            image.file = img_io
        return image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content',
                  'featured_image',]
        labels = {
            'excerpt': 'Short Title',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title').capitalize()
        slug = slugify(title)

        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        self.cleaned_data['slug'] = unique_slug

        return title


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ann Smith'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ann.smith@gmail.com'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'What can we assist you with?'
        })
    )
