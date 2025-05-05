from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime

# Initialize Flask app and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    is_adopted = db.Column(db.Boolean, default=False)

# API Resources
class PetListResource(Resource):
    def get(self):
        pets = Pet.query.all()
        return jsonify([{
            "id": pet.id,
            "name": pet.name,
            "species": pet.species,
            "breed": pet.breed,
            "age": pet.age,
            "description": pet.description,
            "image_url": pet.image_url,
            "is_adopted": pet.is_adopted
        } for pet in pets])

    def post(self):
        data = request.get_json()
        new_pet = Pet(
            name=data['name'],
            species=data['species'],
            breed=data['breed'],
            age=data['age'],
            description=data.get('description'),
            image_url=data.get('image_url'),
            is_adopted=data.get('is_adopted', False)
        )
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({"message": "Pet added successfully", "id": new_pet.id})

class PetResource(Resource):
    def get(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        return jsonify({
            "id": pet.id,
            "name": pet.name,
            "species": pet.species,
            "breed": pet.breed,
            "age": pet.age,
            "description": pet.description,
            "image_url": pet.image_url,
            "is_adopted": pet.is_adopted
        })

    def put(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        data = request.get_json()
        pet.name = data.get('name', pet.name)
        pet.species = data.get('species', pet.species)
        pet.breed = data.get('breed', pet.breed)
        pet.age = data.get('age', pet.age)
        pet.description = data.get('description', pet.description)
        pet.image_url = data.get('image_url', pet.image_url)
        pet.is_adopted = data.get('is_adopted', pet.is_adopted)
        db.session.commit()
        return jsonify({"message": "Pet updated successfully"})

    def delete(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        db.session.delete(pet)
        db.session.commit()
        return jsonify({"message": "Pet deleted successfully"})

# Add API resources
api.add_resource(PetListResource, '/api/pets')
api.add_resource(PetResource, '/api/pets/<int:pet_id>')

# Create database tables
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
