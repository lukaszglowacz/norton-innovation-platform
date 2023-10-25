from django.urls import reverse_lazy
from blog.models import Post
from PIL import Image as PILImage
import os
from blog.forms import CommentForm, PostForm
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Testimonial
from django.contrib.auth.models import User
from random import randint
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.utils.text import slugify
import io
from django.core.files.images import ImageFile
from .views import PostEditForm
from cloudinary.uploader import upload
from django.core.files.base import ContentFile
from django.core import mail
from blog.forms import ContactForm


class PostListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

        # Create some published and draft posts
        self.published_posts = [
            Post.objects.create(
                title=f'Published Post {i}',
                slug=f'published-post-{i}',
                author=self.user,
                content=f'Test Content for Published Post {i}',
                status=1
            ) for i in range(10)
        ]

        self.draft_posts = [
            Post.objects.create(
                title=f'Draft Post {i}',
                slug=f'draft-post-{i}',
                author=self.user,
                content=f'Test Content for Draft Post {i}',
                status=0
            ) for i in range(3)
        ]

    def test_view_url_exists(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_pagination(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['post_list']), 6)

    def test_only_published_posts(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class PostDetailTest(TestCase):
    def setUp(self):
        # Create a user for the test
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Create a test post with the author
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,  # Add this line
            status=1,
            content='Content'
        )

    def test_get_post_detail(self):
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Content')


class PostDetailCommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser' + str(randint(1, 100000)), password='testpass')
        self.client.login(username=self.user.username, password='testpass')

        # Create a test post with the author
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,  # Add this line
            status=1,
            content='Content'
        )

    def test_post_comment(self):
        # Prepare comment data
        comment_data = {
            'body': 'This is a test comment',
        }

        # Post comment
        response = self.client.post(
            reverse('post_detail', args=[self.post.slug]), comment_data, follow=True)

        # Check that the comment was created
        self.assertTrue(Comment.objects.filter(
            body='This is a test comment').exists())

        # Check that the comment is not approved
        self.assertFalse(Comment.objects.get(
            body='This is a test comment').approved)

        # Check that the comment does not appear in the response content
        self.assertNotContains(response, 'This is a test comment')


class PostLikeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            status=1,
            content='Content'
        )

    def test_like_post(self):
        response = self.client.post(
            reverse('post_like', args=[self.post.slug]), follow=True)

        # Check if the post was liked successfully
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

        # Assert that the response redirects to the post detail page
        self.assertRedirects(response, reverse(
            'post_detail', args=[self.post.slug]))

    def test_unlike_post(self):
        # First, add the like
        self.post.likes.add(self.user)

        response = self.client.post(
            reverse('post_like', args=[self.post.slug]), follow=True)

        # Check if the post was unliked successfully
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())

        # Assert that the response redirects to the post detail page
        self.assertRedirects(response, reverse(
            'post_detail', args=[self.post.slug]))


class PostCreateFormTest(TestCase):
    def setUp(self):
        # Create a test user and set up the client
        self.test_user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def create_dummy_image(self, width, height):
        # Create a white image
        image = Image.new("RGB", (width, height), color=(255, 255, 255))

        # Save the image to a BytesIO object
        image_io = BytesIO()
        image.save(image_io, format="JPEG")

        # Create a SimpleUploadedFile from the BytesIO object
        return SimpleUploadedFile("test_image.jpg", image_io.getvalue(), content_type="image/jpeg")

    def test_valid_form_submission(self):
        # Create a dummy image with a width of 800 and height of 600
        dummy_image = self.create_dummy_image(800, 600)

        form_data = {
            'title': 'Test Title',  # Valid title
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',
            'featured_image': dummy_image,
        }
        response = self.client.post(reverse('post_create'), data=form_data)

        # Assertions and validation
        # Redirect to index page after successful form submission
        self.assertEqual(response.status_code, 302)

        # Check that the post is created in the database
        self.assertTrue(Post.objects.filter(title='Test Title').exists())

    def test_invalid_form_submission(self):
        # Create a dummy image file
        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_data, 'jpeg')
        image_data.seek(0)
        dummy_image = SimpleUploadedFile(
            "test_image.jpg", image_data.read(), content_type="image/jpeg")

        form_data = {
            'title': '',  # Empty title, which is invalid
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',
            'featured_image': dummy_image,
        }
        response = self.client.post(reverse('post_create'), data=form_data)

        # Assertions and validation
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_create.html')
        self.assertContains(response, "This field is required.")

        # Check that the post is not created in the database
        self.assertFalse(Post.objects.filter(title='Test Title').exists())

    def test_image_upload(self):
        # Create a dummy image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image
        dummy_image = SimpleUploadedFile(
            "test_image.jpg", image_io.read(), content_type="image/jpeg")

        form_data = {
            'title': 'Test Title',
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',
            'featured_image': dummy_image,
        }

        response = self.client.post(
            reverse('post_create'), data=form_data, format='multipart')
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        # Redirect to the index page
        self.assertEqual(response.url, reverse('index'))

        # Check if the post has been created in the database
        self.assertTrue(Post.objects.filter(title='Test Title').exists())
        new_post = Post.objects.get(title='Test Title')
        # Ensure the image field is not empty
        self.assertTrue(new_post.featured_image)


class PostDeleteTest(TestCase):

    def setUp(self):
        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create another user
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content'
        )

    def test_post_delete_by_author(self):
        # Delete post by author
        response = self.client.post(reverse_lazy(
            'post_delete', args=[self.post.pk]))

        # Assert redirect to index and check post is deleted
        self.assertRedirects(response, reverse_lazy('index'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_by_other_user(self):
        # Login as other user
        self.client.login(username='otheruser', password='testpass')

        # Attempt to delete post by other user
        response = self.client.post(reverse_lazy(
            'post_delete', args=[self.post.pk]))

        # Check if the delete was unsuccessful (could be a redirect to a forbidden page, or 403 status, depending on how you handle unauthorized access)
        self.assertNotEqual(response.status_code, 200)

        # Assert post still exists
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())


class PostEditViewTest(TestCase):
    def setUp(self):
        # Create an author user
        self.author_user = User.objects.create_user(
            username='author', password='testpass')

        # Create another user (not an author of the post)
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass')

        # Create a post authored by the author user
        self.post = Post.objects.create(
            title='Test Post',
            excerpt='Test Excerpt',
            content='Test Content',
            author=self.author_user
        )

    def test_post_edit_by_author(self):
        self.client.login(username='author', password='testpass')
        response = self.client.get(reverse_lazy(
            'post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_by_other_user(self):
        self.client.login(username='otheruser', password='testpass')
        response = self.client.get(reverse_lazy(
            'post_edit', args=[self.post.pk]))
        # Assuming it redirects or forbids access
        self.assertNotEqual(response.status_code, 200)


class PostEditFormTest(TestCase):

    def test_title_max_length(self):
        form_data = {
            'title': 'Test Title' * 10,  # make it longer than 50 characters
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',

        }
        form = PostEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Title can't be longer than 50 characters",
                      form.errors['title'])

    def test_excerpt_max_length(self):
        form_data = {
            'title': 'Test Title',
            'excerpt': 'Test Excerpt' * 20,  # make it longer than 100 characters
            'content': 'Test Content',
        }
        form = PostEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Excerpt can't be longer than 100 characters",
                      form.errors['excerpt'])

    def test_title_is_capitalized(self):
        form_data = {
            'title': 'test title',
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',
        }
        form = PostEditForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test title')

    def create_image(self, name='test_image.jpg', size=(800, 800), image_format='JPEG'):
        image_file = BytesIO()
        image = Image.new('RGB', size)
        image.save(image_file, image_format)
        image_file.seek(0)
        return SimpleUploadedFile(name, image_file.read(), content_type='image/jpeg')

    def test_featured_image_resizing(self):
        # create a mock image file
        image_file = self.create_image()

        # create the form with test data
        form_data = {
            'title': 'Test Title',
            'excerpt': 'Test Excerpt',
            'content': 'Test Content',
            'featured_image': image_file,
        }
        form = PostEditForm(data=form_data)

        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        # This method will run before the execution of each test case.
        self.client = Client()

    def test_contact_form_get(self):
        # Assuming the name of the path is 'contact'
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_form_post_success(self):
        response = self.client.post(reverse('contact'), data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello, this is a test message.'
        })

        # Check if the mail has been sent successfully.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Message from GUOVACH CONSULTING')

        # Assuming 'success' is the name of the path for the success_view.
        self.assertRedirects(response, reverse('success'))

    def test_success_view(self):
        # Assuming the name of the path is 'success'
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success_page.html')
