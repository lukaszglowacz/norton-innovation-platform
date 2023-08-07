from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm, PostForm
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify, capfirst
from django import forms
from django.forms.widgets import Textarea
from django.core.validators import MaxLengthValidator
from PIL import Image
from django.core.files.base import ContentFile
import io



class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True

        comment_form = CommentForm(data=request.POST, files=request.FILES)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request, 'Your comment is awaiting approval')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        error_messages={
            'max_length': "Title can't be longer than 50 characters"
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your title here'}
        )
    )
    excerpt = forms.CharField(
        max_length=100,
        error_messages={
            'max_length': "Excerpt can't be longer than 100 characters"
        },
        widget=forms.Textarea(
            attrs={'rows': 2, 'cols': 40,
                   'placeholder': 'Enter your short title here'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'featured_image']
        labels = {
            'featured_image': 'Upload image'
        }
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 6, 'cols': 40, 'placeholder': "Share your inspiration for this wall! Whether it's a bold geometric pattern or a calming landscape, tell us what motivates your design"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return capfirst(title)

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['excerpt'].label = "Short Title"

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image', False)
        if image:
            img = Image.open(image)
            max_size = (800, 800)  # Max size (width, height)
            img.thumbnail(max_size, Image.LANCZOS)
            img_io = io.BytesIO()
            img_format = img.format if img.format else 'JPEG'  # Corrected indentation
            img.save(img_io, format=img_format, quality=60)
            img_io.seek(0)  # Reset file pointer to the beginning
            image.name = 'resized_' + image.name  # Change the image filename
            # Create a new Django file-like object
            image.file = img_io
        return image


class PostCreate(View):
    def get(self, request):
        form = PostCreateForm()  # Using the new form class
        return render(request, "post_create.html", {"form": form})

    def post(self, request):
        # Using the new form class
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(form.cleaned_data['title'])
            post.status = 1
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "post_create.html", {"form": form})


class PostEditForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        error_messages={
            'max_length': "Title can't be longer than 50 characters"
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your title here'}
        )
    )

    excerpt = forms.CharField(
        max_length=100,
        label='Short Title',
        error_messages={
            'max_length': "Excerpt can't be longer than 100 characters"
        },
        widget=forms.Textarea(
            attrs={'rows': 2, 'cols': 40,
                   'placeholder': 'Enter your short title here'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'featured_image']
        labels = {
            'featured_image': 'Upload image'
        }
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 6, 'cols': 40, 'placeholder': "Share your inspiration for this wall! Whether it's a bold geometric pattern or a calming landscape, tell us what motivates your design"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return capfirst(title)

    def clean_featured_image_edit(self):
        image = self.cleaned_data.get('featured_image', False)
        if image:
            # Check if the image is a file upload or a CloudinaryResource object
            if hasattr(image, 'read'):
                img = Image.open(image)
            else:  # Assume it's a CloudinaryResource object
                response = requests.get(image.url)
                img = Image.open(io.BytesIO(response.content))
            max_size = (800, 800)  # Max size (width, height)

            img.thumbnail(max_size, Image.LANCZOS)
            img_io = io.BytesIO()
            img_format = img.format if img.format else 'JPEG'
            img.save(img_io, format=img_format, quality=60)
            img_io.seek(0)  # Reset file pointer to the beginning
            image.name = 'resized_' + image.name  # Change the image filename

            # Create a new Django file-like object
            image = ContentFile(img_io.read(), name=image.name)
            img_io.close()
        return image


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user