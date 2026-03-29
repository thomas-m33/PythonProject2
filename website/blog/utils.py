from django.db.models import Q
from .models import Post

def visible_posts(user):
    qs = Post.objects.select_related("author", "author__profile")

    if user.is_authenticated:
        return qs.filter(
            Q(author=user) |
            Q(author__profile__posts_private=False) |
            Q(author__profile__trusted_users=user)
        ).distinct()
    # Q(A) | Q(B) | Q(C) collects posts that satisfy condition A, condition B, or condition C.
    # Since posts may satisfy multiple of these at once, .distinct() is used to get the unique ones.

    return qs.filter(author__profile__posts_private=False)
    # returns posts that aren't private if user is not signed in