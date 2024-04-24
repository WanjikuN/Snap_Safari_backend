from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from models import db, User, Album, Photo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snap_safari.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app)

# Define fields for marshalling
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String
}

album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'users_id': fields.Integer
}

photo_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'image_url': fields.String,
    'album_id': fields.Integer,
}

class UserResource(Resource):
    
    @marshal_with(user_fields)
    def get(self, users_id):
        user = User.query.get_or_404(users_id)
        return user

    
    @marshal_with(user_fields)
    def put(self, users_id):
        user = User.query.get_or_404(users_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        user.name = args['name']
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user

    def delete(self, users_id):
        user = User.query.get_or_404(users_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserListResource(Resource):
    
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        user = User(name=args['name'], username=args['username'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class AlbumResource(Resource):
    
    @marshal_with(album_fields)
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        return album

class AlbumListResource(Resource):
    
    @marshal_with(album_fields)
    def get(self):
        albums = Album.query.all()
        return albums

class PhotoResource(Resource):
    
    @marshal_with(photo_fields)
    def get(self, photo_id):
        photo = Photo.query.get_or_404(photo_id)
        return photo

    @marshal_with(photo_fields)
    def patch(self, photo_id):
        photo = Photo.query.get_or_404(photo_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('image_url', type=str, required=True)
        parser.add_argument('album_id', type=int, required=True)
        args = parser.parse_args()
        photo.title = args['title']
        photo.image_url = args['image_url']
        photo.album_id = args['album_id']
        db.session.commit()
        return photo

class PhotoListResource(Resource):
    
    @marshal_with(photo_fields)
    def get(self):
        photos = Photo.query.all()
        return photos

api.add_resource(UserResource, '/users/<int:users_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(AlbumResource, '/albums/<int:album_id>')
api.add_resource(AlbumListResource, '/albums')
api.add_resource(PhotoResource, '/photos/<int:photo_id>')
api.add_resource(PhotoListResource, '/photos')

if __name__ == '__main__':
    app.run(debug=True)
