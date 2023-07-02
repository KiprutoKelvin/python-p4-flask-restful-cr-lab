#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self, plant_id=None):
        if plant_id:
            plant = Plant.query.get(plant_id)
            if not plant:
                return {'message': 'Plant not found'}, 404
            return {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            }
        else:
            plants = Plant.query.all()
            return [{
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            } for plant in plants]

    def post(self):
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()

        return {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        }, 201

api.add_resource(Plants, '/plants', '/plants/<int:plant_id>')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if not plant:
            return {'message': 'Plant not found'}, 404
        return {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        }
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
