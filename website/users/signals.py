import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver

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
