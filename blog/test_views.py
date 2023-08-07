import os
from .models import Post
from blog.forms import CommentForm, PostForm
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment
from django.contrib.auth.models import User
from random import randint
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


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
