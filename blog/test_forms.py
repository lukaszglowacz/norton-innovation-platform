from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from .forms import CommentForm, PostForm
from django.test import TestCase
from .models import Comment, Post


class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        # Creating an in-memory image file for testing
        image_file = BytesIO()
        image = Image.new('RGBA', size=(1000, 1000), color=(256, 0, 0))
        image.save(image_file, 'png')
        image_file.seek(0)

        # Creating a SimpleUploadedFile object to simulate an uploaded image
        image_upload = SimpleUploadedFile(
            name='test_image.png',
            content=image_file.read(),
            content_type='image/png'
        )

        # Test data for form submission
        form_data = {
            'body': 'Test Comment',
            'image': image_upload
        }

        # Make sure to include the file in the form
        form = CommentForm(data=form_data, files={'image': image_upload})

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

        # Assert that the image has been resized
        # Get the cleaned image from the form's cleaned_data
        cleaned_image = form.cleaned_data['image']
        img = Image.open(cleaned_image)
        self.assertTrue(img.size[0] <= 800 and img.size[1] <= 800)

        # Assert that the filename is prefixed with 'resized_'
        self.assertTrue(cleaned_image.name.startswith('resized_'))


class PostFormTest(TestCase):
    def test_post_form_valid(self):
        # You can create a SimpleUploadedFile for the featured_image field if needed
        image_file = BytesIO()
        image = Image.new('RGBA', size=(1000, 1000), color=(256, 0, 0))
        image.save(image_file, 'png')
        image_file.seek(0)

        featured_image = SimpleUploadedFile(
            name='featured_image.png',
            content=image_file.read(),
            content_type='image/png'
        )

        # Test data for form submission
        form_data = {
            'title': 'test title',
            'excerpt': 'Test excerpt',
            'content': 'Test content',
            'featured_image': featured_image,
        }

        form = PostForm(data=form_data, files={
                        'featured_image': featured_image})

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

        # Assert that the title is capitalized
        cleaned_title = form.clean_title()
        self.assertEqual(cleaned_title, 'Test title')

        # Assert that the slug is unique
        slug = form.cleaned_data['slug']
        self.assertFalse(Post.objects.filter(slug=slug).exists())
