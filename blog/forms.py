from .models import Comment, Post
from django import forms
from django.utils.text import slugify


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content',
                  'featured_image', 'excerpt',]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)

        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        self.cleaned_data['slug'] = unique_slug

        return title
