import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    logger.info("Successful login: user=%s", user.username)

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get("username", "unknown")
    logger.warning("Failed login attempt: user=%s", username)

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    logger.info("User logged out: user=%s", user.username)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    instance.profile.save()