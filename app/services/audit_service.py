from app.models import AuditLog
from app.extensions import db
from flask import request

class AuditService:
    @staticmethod
    def log(action: str, admin_id: int = None, target_entity: str = '', target_id: str = '', details: str = ''):
        """
        Records an administrative or sensitive platform action in the audit log.
        """
        ip = request.remote_addr if request else '127.0.0.1'
        log_entry = AuditLog(
            admin_id=admin_id,
            action=action,
            target_entity=target_entity,
            target_id=str(target_id),
            details=details,
            ip_address=ip
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
