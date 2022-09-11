# app.py
import json

from flask import Flask, request
from flask_restx import Api, Resource
from marshmallow import Schema, fields
from config import app, db
from models import Movie
from schemas import MovieSchema


api = Api(app)


movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genre')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        query = Movie.query
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        return MovieSchema(many=True).dump(Movie.query.all()), 200


    def post(self):
        """
        Добавляем данные.
        """
        data = request.json
        try:
            db.session.add(
                Movie(**data)
            )
            db.session.commit()
            return "Успешно добавлено", 201
        except Exception as e:
            db.session.rollback()
            return "Не добавлен", 500


@movie_ns.route('/<int:id>')
class MoviesView(Resource):
    def get(self, id):
        res = db.session.query(Movie).filter(Movie.id == id).all()
        if len(res):
            return MovieSchema().dump(res[0]), 200
        else:
            return json.dumps({}), 200


    def put(self, id):
        """
        Обновляем данные.
        """
        data = request.json
        try:
            res = Movie.query.filter(Movie.id == id).one()
            res.title = data.get('title')  # Обновляем только title, можно добавить столбы.
            db.session.add(res)
            db.session.commit()
            return "Название/Описание обновилось", 200
        except Exception:
            db.session.rollback()
            return "Не обновилось", 200


    def delete(self, id):
        """
        Удаляем данные.
        """
        try:
            res = Movie.query.filter(Movie.id == id).one()
            db.session.delete(res)
            db.session.commit()
            return "Успешно удалено", 200
        except Exception:
            db.session.rollback()
            return "Не удалили", 200


if __name__ == '__main__':
    app.run(debug=True)
