from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # categories are just text (e.g. 'Business') so they use a CharField

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    categories = models.ManyToManyField(Category, blank=True, related_name="posts")
    # One post can have many categories and one categories can have many posts (many to many)

    tags = TaggableManager(blank=True)
    # Many-to-many relationship between tags and posts. blank=True makes the tags field optional


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



