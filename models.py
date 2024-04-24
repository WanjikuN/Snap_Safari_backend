#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()
userAlbums_association = db.Table(
    'user_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'))
)
class User(db.Model, SerializerMixin):
    __tablename__ ='users'

    serialize_rules = ('-albums',)

    #columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String) 
    username = db.Column(db. String, unique=True)
    email = db.Column(db.String, unique=True)

    #relationships
    albums = db.relationship('Album', secondary = userAlbums_association, back_populates='users')


class Album(db.Model, SerializerMixin):
    __tablename__ ='albums'
    serialize_rules = ('-users',)

    #columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.column(db.String) 
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships
    users = db.relationship('User', secondary=userAlbums_association, back_populates='albums')


class Photo(db.Model, SerializerMixin):
    __tablename__ ='photos'

    serialize_rules = ('-albums.photos',)

    #columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String) 
    image_url = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    
    # relationships
    albums = db.relationship('Album', backref='photos')


