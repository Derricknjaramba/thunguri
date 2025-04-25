from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

    @staticmethod
    def admin_exists():
        """
        Check if an admin already exists in the database.
        """
        return db.session.query(User.id).filter_by(is_admin=True).first() is not None


# Nursery model for Admin and Guest resources
class Nursery(db.Model):
    """Nursery model representing a nursery."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    photo_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Nursery {self.name}>"

    
# Product model for Admin and Guest resources
class Product(db.Model):
    """Product model representing a product in the system."""
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"


# AboutUs model for Admin and Guest resources
class AboutUs(db.Model):
    """AboutUs model providing details about the organization."""
    __tablename__ = 'about_us'
    id = db.Column(db.Integer, primary_key=True)
    who_we_are = db.Column(db.Text, nullable=True)
    our_story = db.Column(db.Text, nullable=True)
    mission_statement = db.Column(db.Text, nullable=True)
    vision = db.Column(db.Text, nullable=True)
    core_values = db.Column(db.Text, nullable=True)
    what_we_do = db.Column(db.Text, nullable=True)
    why_choose_us = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<AboutUs {self.id}>"


# MillingProcess model (Admin & Guest Resources)
class MillingProcess(db.Model):
    """Milling process model representing various milling processes."""
    __tablename__ = 'milling_processes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    video_link = db.Column(db.String(200), nullable=True)  # Changed from video_path to video_link

    def __repr__(self):
        return f"<MillingProcess {self.name}>"


# AggressionProcess model (Admin & Guest Resources)
class AggressionProcess(db.Model):
    """Aggression process model representing various aggression processes."""
    __tablename__ = 'aggression_processes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    video_link = db.Column(db.String(200), nullable=True)  # Changed from video_path to video_link

    def __repr__(self):
        return f"<AggressionProcess {self.name}>"


# FarmProgression model (Admin & Guest Resources)
class FarmProgression(db.Model):
    """Farm progression model representing various farm progressions."""
    __tablename__ = 'farm_progressions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    photo_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<FarmProgression {self.name}>"


# HowTo model (Admin & Guest Resources)
class HowTo(db.Model):
    """HowTo model for providing instructional content."""
    __tablename__ = 'how_tos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    video_link = db.Column(db.String(200), nullable=True)  # Changed to video_link

    def __repr__(self):
        return f"<HowTo {self.title}>"


# Announcement model (Admin & Guest Resources)
class Announcement(db.Model):
    """Announcement model for storing organizational announcements."""
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Announcement {self.title}>"












