#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import json
# from lib2to3.pgen2.pgen import generate_grammar
# from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine
from dotenv import load_dotenv
load_dotenv()

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#

database_name = os.getenv('DB_NAME')
database_user = os.getenv('DB_USER')
database_pwd = os.getenv('DB_PASS')
database_host = os.getenv('DB_HOST')
database_path = "postgresql://{}/{}".format(database_host, database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Super Class for Models
#----------------------------------------------------------------------------#

class Operations:
    def __init__(self) -> None:
        pass

    def flush(self):
        db.session.add(self)
        db.session.flush()
        print('Flushed! You can now grab the ID before it is updated to the DB')

    def insert(self):
        db.session.add(self)
        db.session.commit()
        print('Inserted!')
    
    def update(self):
        db.session.commit()
        print('Updated!')

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        print('Deleted!')
    
    def undo(self):
        db.session.rollback()
        print('Undone!')

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

class Movie(db.Model, Operations):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(40), nullable=False)
    genre = Column(String(40), nullable=False)
    release_date = Column(Date, nullable=False)
    director = Column(String(40), nullable=False)
    commitments = db.relationship('Commitment', backref='movies', lazy=True, cascade='all, delete-orphan')
    roles = db.relationship('Role', backref='movies', lazy=True, cascade='all, delete-orphan')

    def __init__(self, movie_name, genre, release_date, director):
        Operations.__init__(self)
        self.movie_name = movie_name
        self.genre = genre
        self.release_date = release_date
        self.director = director
    
    
    def format(self):
        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'genre': self.genre,
            'release_date': self.release_date,
            'director': self.director
        }


class Actor(db.Model, Operations):
    __tablename__ = 'actors'

    actor_id = Column(Integer, primary_key=True)
    actor_name = Column(String(40), nullable=False)
    phone = Column(String(40), nullable=False)
    age = Column(String(3), nullable=False)
    gender = Column(String(1), nullable=False)
    image_link = Column(String(500), nullable=False)
    commitments = db.relationship('Commitment', backref='actors', lazy=True, cascade='all, delete-orphan')

    def __init__(self, actor_name, phone, age, gender, image_link):
        Operations.__init__(self)
        self.actor_name = actor_name
        self.phone = phone
        self.age = age
        self.gender = gender
        self.image_link = image_link
    
    def format(self):
        return {
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'age': self.age,
            'gender': self.gender,
            'image_link': self.image_link
        }


class Commitment(db.Model, Operations):
    __tablename__ = 'commitments'

    commitment_id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.actor_id'), nullable=False)
    role_type_id = Column(Integer, ForeignKey('role_types.role_types_id'), nullable=False)

    def __init__(self, start_date, end_date, movie_id, actor_id, role_type_id):
        self.start_date = start_date
        self.end_date = end_date
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.role_type_id = role_type_id

    def format(self):
        return {
            'commitment_id': self.commitment_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'role_type_id': self.role_type_id
        }


class Role(db.Model, Operations):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_number = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    role_type_id = Column(Integer, ForeignKey('role_types.role_types_id'), nullable=False)

    def __init__(self, role_number, movie_id, role_type_id):
        self.role_number = role_number
        self.movie_id = movie_id
        self.role_type_id = role_type_id

    def format(self):
        return {
            'role_id': self.role_id,
            'number': self.role_number,
            'movie_id': self.movie_id,
            'role_type_id': self.role_type_id
        }


class RoleType(db.Model, Operations):
    __tablename__ = 'role_types'

    role_types_id = Column(Integer, primary_key=True)
    role_type = Column(String(20), nullable=False)
    commitments = db.relationship('Commitment', backref='role_types', lazy=True, cascade='all, delete-orphan')
    roles = db.relationship('Role', backref='role_types', lazy=True, cascade='all, delete-orphan')

    def __init__(self, role_type):
        self.role_type = role_type

    def format(self):
        return {
            'role_types_id': self.role_types_id,
            'role_type': self.role_type
        }