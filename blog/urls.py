from . import views
from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('index/', views.PostList.as_view(), name='index'),
    path('new/', PostCreate.as_view(), name='post_create'),
    path('contact/', views.contact_form, name='contact'),
    path('success/', views.success_view, name='success'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
