"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://unsplash.com/photos/black-framed-sunglasses-on-white-surface-lSl94SZHRgA'

 
def connect_db(app):
    """connect database to this flask app"""
        
    db.app = app
    db.init_app(app)

class User(db.Model):
    """creates new user"""
    
    __tablename__= 'users'    
    
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.Text, nullable= False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)
    
    posts = db.relationship('Post', backref='user', cascade= 'all, delete-orphan')
    
    @property
    def full_name(self):
        """Returns full name of user"""
        
        return f"{ self.first_name} { self. last_name}"
    
class Post(db.Model):
    """ generate BLOG POST"""
    
    __tablename__= 'posts'
    
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.Text, nullable=False)
    content= db.Column(db.Text, nullable=False)
    created_at= db.Column(
        db.DateTime,
        nullable=False,
        default= (datetime, datetime.now))
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    @property
    def pretty_date(self):
        
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    
class PostTag(db.Model):
    """create tag on post"""
    
    __tablename__ = 'posts_tags'
    
    post_id=db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id= db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True)
    
class Tags(db.Model):
    """Tags to post """
    
    __tablename__= 'tags'
    
    id= db.Column(db.Integer, primary_key=True) 
    name= db.Column(db.Text, nullable=False, unique=True) 
    
    posts= db.relationship('Post', secondary='posts_tags', cascade='all, delete', backref='tags')
      


def connect_db(app):
    db.app = app
    db.init_app(app)