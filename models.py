
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    
    ai_usage_count = db.Column(db.Integer, default=0)
    last_usage_date = db.Column(db.String(20), nullable=True)
    # New future-safe premimum field
    is_premimum = db.Column(db.Boolean, default=False)
    
    
    # Relationship to link resumes to a user
    resumes = db.relationship('Resume', backref='owner', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # We store the resume data as separate fields for easy editing
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    education = db.Column(db.Text)  # Store as string or structured text
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    projects = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)