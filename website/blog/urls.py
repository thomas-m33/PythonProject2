from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # pk is a primary key that Django uses to identify which post the view is being loaded for
    path('about/', views.about, name='blog-about'),
]