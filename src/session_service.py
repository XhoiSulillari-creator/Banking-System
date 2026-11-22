import secrets
from datetime import datetime, timedelta


class SessionService:

    def __init__(self, session_duration_minutes=15):
        self.sessions = {}
        self.session_duration = timedelta(
            minutes=session_duration_minutes
        )

    def create_session(self, identity):
        token = secrets.token_urlsafe(32)

        self.sessions[token] = {
            "identity": identity,
            "expires_at": datetime.now() + self.session_duration
        }

        return token

    def get_identity(self, token):
        session = self.sessions.get(token)

        if session is None:
            return None

        if datetime.now() >= session["expires_at"]:
            del self.sessions[token]
            return None

        return session["identity"]

    def invalidate_session(self, token):
        self.sessions.pop(token, None)