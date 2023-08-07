from django.test import TestCase
from .forms import CommentForm
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


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

        form = CommentForm(data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

        # Assert that the image has been resized
        cleaned_image = form.clean_image()
        img = Image.open(cleaned_image)
        self.assertTrue(img.size[0] <= 800 and img.size[1] <= 800)

        # Assert that the filename is prefixed with 'resized_'
        self.assertTrue(cleaned_image.name.startswith('resized_'))
