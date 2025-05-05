#############Imports####################
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#############Imports####################
    
"""
This Script creates a SQL database with the tables User, Library and SubgenrePlot
"""
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_title = db.Column(db.String(255), nullable=False)
    book_authors = db.Column(db.String(255), nullable=False)
    book_cover = db.Column(db.String(255), nullable=False)
    book_description = db.Column(db.Text, nullable=False)
    book_rating = db.Column(db.Float, nullable=False)
    book_playlist = db.Column(db.String(255), nullable=True)
    book_playlistname = db.Column(db.String, nullable=True)
    umbrella_genre = db.Column(db.String(255), nullable=True)
    subgenres = db.Column(db.String(255), nullable=True)
    percentages = db.Column(db.Text, nullable=True)

class SubgenrePlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), unique=True, nullable=False)
    plot_data = db.Column(db.Text, nullable=False)
