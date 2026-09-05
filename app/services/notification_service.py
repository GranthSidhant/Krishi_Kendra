from app.models import Notification
from app.extensions import db

class NotificationService:
    @staticmethod
    def send(user_id: int, title: str, message: str, link_url: str = '#') -> Notification:
        """
        Creates an in-app notification for a user.
        """
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            link_url=link_url,
            is_read=False
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def get_user_notifications(user_id: int, limit: int = 15):
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(limit).all()
