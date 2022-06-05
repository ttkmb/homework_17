# app.py
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


class DirectorsSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenresSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)
directors_schema = DirectorsSchema(many=True)
genres_schema = GenresSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        all_movies = Movie.query
        if director_id:
            all_movies = all_movies.filter(Movie.director_id == director_id)
        if genre_id:
            all_movies = all_movies.filter(Movie.genre_id == genre_id)
        all_movies = all_movies.all()
        return movies_schema.dump(all_movies), 200


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200


@directors_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        data = request.get_json()
        new_director = Director(**data)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()
        return '', 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def put(self, did: int):
        director = Director.query.get(did)
        data = request.get_json()
        director.id = data.get("id")
        director.name = data.get("name")
        db.session.add(director)
        db.session.commit()
        db.session.close()
        return '', 200

    def delete(self, did: int):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        db.session.close()
        return '', 200


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genre = Genre.query.all()
        return genres_schema.dump(genre), 200

    def post(self):
        data = request.get_json()
        new_genre = Genre(**data)
        db.session.add(new_genre)
        db.session.commit()
        db.session.close()
        return '', 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def put(self, gid: int):
        genre = Genre.query.get(gid)
        data = request.get_json()
        genre.id = data.get("id")
        genre.name = data.get("name")
        db.session.add(genre)
        db.session.commit()
        db.session.close()
        return '', 200

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        db.session.close()
        return '', 200


if __name__ == '__main__':
    app.run(debug=True)
