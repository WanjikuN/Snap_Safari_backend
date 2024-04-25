from flask import Flask
from faker import Faker
from models import db, User, Album, Photo
from random import randint
from datetime import datetime
import random

import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snap_safari.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
fake = Faker()


def clear_tables():
        # Clear all records from the tables
        # db.session.query(User).delete()
        # db.session.query(Album).delete()
        # db.session.query(Photo).delete()

        # Commit the changes to the database
        db.session.commit()
def create_users(num_users):
    users = []
    for _ in range(num_users):
        user = User(
            name=fake.name(),
            username=fake.user_name(),
            email=fake.email()
        )
        users.append(user)
    return users


def create_albums(num_albums, users):
    albums = []
    for _ in range(num_albums):
        user = random.choice(users)
        album = Album(
            title=fake.sentence(),
            users_id=user.id  
        )
        albums.append(album)
    return albums


def create_photos(num_photos, albums):
    photos = []
    for _ in range(num_photos):
        photo = Photo(
            title=fake.sentence(),
            image_url=fake.image_url(),
            album_id=randint(1, len(albums))
        )
        photos.append(photo)
    return photos



if __name__ == '__main__':
    with app.app_context():
        clear_tables()
        db.create_all()
        num_users = 10
        num_albums = 20
        num_photos = 50

        users = create_users(num_users)
        db.session.add_all(users)
        db.session.commit()

        albums = create_albums(num_albums, users)
        db.session.add_all(albums)
        db.session.commit()

        photos = create_photos(num_photos, albums)
        db.session.add_all(photos)
        db.session.commit()

