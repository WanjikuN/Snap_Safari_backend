from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from models import db, User, Album, Photo
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snap_safari.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app, version='1.0', title='SnapSafari API',
          description='An API for managing users, albums, and photos')
CORS(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:36859"]}}, supports_credentials=True)

user_fields = api.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String
})

album_fields = api.model('Album', {
    'id': fields.Integer,
    'title': fields.String,
    'user_id': fields.Integer
})

photo_fields = api.model('Photo', {
    'id': fields.Integer,
    'title': fields.String,
    'image_url': fields.String,
    'album_id': fields.Integer,
})

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)

user_ns = api.namespace('users', description='User operations')
album_ns = api.namespace('albums', description='Album operations')
photo_ns = api.namespace('photos', description='Photo operations')

@user_ns.route('/')
class UserListResource(Resource):
    @user_ns.marshal_list_with(user_fields)
    def get(self):
        return User.query.all()

    @user_ns.expect(user_fields)
    @user_ns.marshal_with(user_fields, code=201)
    def post(self):
        args = parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @user_ns.marshal_with(user_fields)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    @user_ns.expect(user_fields)
    @user_ns.marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = parser.parse_args()
        user.update(args)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

@album_ns.route('/')
class AlbumListResource(Resource):
    @album_ns.marshal_list_with(album_fields)
    def get(self):
        return Album.query.all()

    @album_ns.expect(album_fields)
    @album_ns.marshal_with(album_fields, code=201)
    def post(self):
        args = parser.parse_args()
        album = Album(**args)
        db.session.add(album)
        db.session.commit()
        return album, 201

@album_ns.route('/<int:album_id>')
@album_ns.param('album_id', 'The album identifier')
class AlbumResource(Resource):
    @album_ns.marshal_with(album_fields)
    def get(self, album_id):
        return Album.query.get_or_404(album_id)

@photo_ns.route('/')
class PhotoListResource(Resource):
    @photo_ns.marshal_list_with(photo_fields)
    def get(self):
        return Photo.query.all()

@photo_ns.route('/<int:photo_id>')
@photo_ns.param('photo_id', 'The photo identifier')
class PhotoResource(Resource):
    @photo_ns.marshal_with(photo_fields)
    def get(self, photo_id):
        return Photo.query.get_or_404(photo_id)

    @photo_ns.expect(photo_fields)
    @photo_ns.marshal_with(photo_fields)
    def patch(self, photo_id):
        photo = Photo.query.get_or_404(photo_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        args = parser.parse_args()
        if 'title' in args:
            photo.title = args['title']

        db.session.commit()
        return photo
if __name__ == '__main__':
    app.run(debug=True)
