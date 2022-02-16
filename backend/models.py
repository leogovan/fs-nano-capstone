#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
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


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    phone = Column(String(40), nullable=False)
    age = Column(String(3), nullable=False)
    gender = Column(String(1), nullable=False)
    image_link = Column(String(500), nullable=False)


class Commitment(db.Model):
    __tablename__ = 'commitments'

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    role_type_id = Column(Integer, ForeignKey('role_types.id'), nullable=False)


class RoleType(db.Model):
    __tablename__ = 'role_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(40), nullable=False)