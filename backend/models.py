#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from lib2to3.pgen2.pgen import generate_grammar
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    genre = Column(String(40), nullable=False)
    release_date = Column(Date, nullable=False)
    director = Column(String(40), nullable=False)
    commitments = db.relationship('Commitment', backref='movies', lazy=True, cascade='all, delete-orphan')
    roles = db.relationship('Role', backref='movies', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, genre, release_date, director, commitments, roles):
        self.name = name
        self.genre = genre
        self.release_date = release_date
        self.director = director
        self.commitments = commitments
        self.roles = roles
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'release_date': self.release_date,
            'director': self.director,
            'commitments': self.commitments,
            'roles': self.roles
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    phone = Column(String(40), nullable=False)
    age = Column(String(3), nullable=False)
    gender = Column(String(1), nullable=False)
    image_link = Column(String(500), nullable=False)
    commitments = db.relationship('Commitment', backref='actors', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, phone, age, gender, image_link, commitments):
        self.name = name
        self.phone = phone
        self.age = age
        self.gender = gender
        self.image_link = image_link
        self.commitments = commitments
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image_link': self.image_link,
            'commitments': self.commitments
        }


class Commitment(db.Model):
    __tablename__ = 'commitments'

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    role_type_id = Column(Integer, ForeignKey('role_types.id'), nullable=False)

    def __init__(self, start_date, end_date, movie_id, actor_id, role_type_id):
        self.start_date = start_date
        self.end_date = end_date
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.role_type_id = role_type_id

    def format(self):
        return {
            'id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'role_type_id': self.role_type_id
        }


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    role_type_id = Column(Integer, ForeignKey('role_types.id'), nullable=False)

    def __init__(self, number, movie_id, role_type_id):
        self.number = number
        self.movie_id = movie_id
        self.role_type_id = role_type_id

    def format(self):
        return {
            'id': self.id,
            'number': self.number,
            'end_date': self.end_date,
            'movie_id': self.movie_id,
            'role_type_id': self.role_type_id
        }


class RoleType(db.Model):
    __tablename__ = 'role_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(40), nullable=False)
    commitments = db.relationship('Commitment', backref='role_types', lazy=True, cascade='all, delete-orphan')
    roles = db.relationship('Role', backref='role_types', lazy=True, cascade='all, delete-orphan')

    def __init__(self, type, commitments, roles):
        self.type = type
        self.commitments = commitments
        self.roles = roles

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'commitments': self.commitments,
            'roles': self.roles
        }