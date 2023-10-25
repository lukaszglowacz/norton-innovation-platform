from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Testimonial
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import tempfile
from PIL import Image


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Title',
            slug='test-title',
            author=self.user,
            content='Test Content',
            status=1
        )

    def test_post_creation(self):
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.__str__(), 'Test Title')

    def test_post_ordering(self):
        self.assertEqual(str(Post._meta.ordering[0]), '-created_on')

    def test_number_of_likes(self):
        self.assertEqual(self.post.number_of_likes(), 0)
        self.post.likes.add(self.user)
        self.assertEqual(self.post.number_of_likes(), 1)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test Content for Post',
            status=1
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name='Comment Author',
            email='author@example.com',
            body='Test comment body',
            approved=False
        )

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(
            self.comment.__str__(), 'Comment Test comment body by Comment Author')

    def test_comment_ordering(self):
        self.assertEqual(str(Comment._meta.ordering[0]), 'created_on')

    def test_comment_approval(self):
        self.assertFalse(self.comment.approved)
        self.comment.approved = True
        self.comment.save()
        self.assertTrue(Comment.objects.get(id=self.comment.id).approved)


class TestimonialModelTest(TestCase):

    def setUp(self):
        # Create a temporary image
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new("RGB", (100, 100))
        image.save(self.temp_file, 'jpeg')

        # Important: reset the file pointer to the beginning of the file.
        self.temp_file.seek(0)

        # Now that you have a 'real' file, you can create the Testimonial instance
        self.testimonial = Testimonial.objects.create(
            name='John Doe',
            title='CEO of TechWorld',
            testimonial_text='This platform is incredibly helpful.',
            image=SimpleUploadedFile(name='test_image.jpg',
                                     content=self.temp_file.read(),
                                     content_type='image/jpeg')  # Here, we're reading content from the temp file
        )

        # Make sure to close the temp file at the end of the test run
        self.temp_file.close()

    def test_testimonial_creation(self):
        """
        Test if the Testimonial object is created with the expected attributes
        """
        # Fetch the testimonial that was supposedly saved to the database
        saved_testimonial = Testimonial.objects.get(name='John Doe')

        # Now assert that the object was indeed saved and is retrieved correctly
        self.assertEqual(saved_testimonial, self.testimonial)

    def test_string_representation(self):
        """
        Test the string representation of the Testimonial model.
        It should return the model's 'name' field.
        """
        self.assertEqual(str(self.testimonial), 'John Doe')

    def tearDown(self):
        # Delete the temporary file
        # Django also deletes the file from storage backend when you delete the model
        self.testimonial.delete()
        super().tearDown()  # Call the tearDown from the superclass
