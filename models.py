from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    
    idusers = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fristname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    email = db.Column(db.String(100))  # Increased for longer emails
    passwrod = db.Column(db.String(255), nullable=False)  # Increased for password hash
    lastpassword = db.Column(db.String(255))  # Increased for password hash
    createat = db.Column(db.String(45), nullable=False, default=lambda: datetime.now().isoformat())
    updateat = db.Column(db.String(45))
    role = db.Column(db.String(45))

class Bank(db.Model):
    __tablename__ = 'back'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    back_name = db.Column(db.String(45))
    back_code = db.Column(db.String(45))
    back_account = db.Column(db.String(45))
    amount = db.Column(db.Numeric(15, 2))
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.String(36), nullable=False)  # Changed to String(36) to match UUID format
