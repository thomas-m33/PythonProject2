from django.contrib.sessions.models import Session
from django.utils import timezone

def logout_all_sessions(user, current_session_key=None):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    # filters for sessions which haven't expired (expire date >= current time)
    for session in sessions:
        if current_session_key and session.session_key == current_session_key:
            continue # don't delete the session if it's the same session which reset the password
        session_data = session.get_decoded()
        if session_data.get('_auth_user_id') == str(user.id):
            session.delete() # deletes sessions belonging to user