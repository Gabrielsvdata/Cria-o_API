from src.model import db
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime
from datetime import datetime, timedelta
import uuid

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    token = Column(String(36), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)

    @classmethod
    def create(cls, email):
        token = str(uuid.uuid4())
        expires = datetime.utcnow() + timedelta(hours=1)
        pr = cls(email=email, token=token, expires_at=expires)
        db.session.add(pr)
        db.session.commit()
        return pr