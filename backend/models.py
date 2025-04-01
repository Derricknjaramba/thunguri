from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Product model for Admin and Guest resources
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"

# Nursery model for Admin and Guest resources
class Nursery(db.Model):
    __tablename__ = 'nurseries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    photo_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Nursery {self.name}>"

# AboutUs model for Admin and Guest resources
class AboutUs(db.Model):
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
    __tablename__ = 'milling_processes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    video_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<MillingProcess {self.name}>"

# AggressionProcess model (Admin & Guest Resources)
class AggressionProcess(db.Model):
    __tablename__ = 'aggression_processes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    video_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<AggressionProcess {self.name}>"

# FarmProgression model (Admin & Guest Resources)
class FarmProgression(db.Model):
    __tablename__ = 'farm_progressions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    photo_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<FarmProgression {self.name}>"

# HowTo model (Admin & Guest Resources)
class HowTo(db.Model):
    __tablename__ = 'how_tos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    video_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<HowTo {self.title}>"

# Announcement model (Admin & Guest Resources)
class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Announcement {self.title}>"






