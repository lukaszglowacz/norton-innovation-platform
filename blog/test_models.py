from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


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
