import os
from app import create_app, db
from app.models import Pet, User
from werkzeug.security import generate_password_hash

def main():
    app = create_app()
    with app.app_context():
        
        db.drop_all()
        db.create_all()
  
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('password', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            print("Created admin user 'admin' with password 'password'.")

        
        pets_info = [
            {"image": "cat1.jpg", "species": "Cat", "name": "Caramel", "age": 2,   "breed": "Domestic Shorthair",   "description": "Color: Orange Tabby", "address": "123 Cat Lane", "city": "Pawville", "phone_number": "555-123-432"},
            {"image": "cat2.jpg", "species": "Cat", "name": "Luna",    "age": 1.5, "breed": "Ragdoll",             "description": "Color: Seal Bicolor", "address": "456 Cat Street", "city": "Meowtown", "phone_number": "555-987-654"},
            {"image": "cat3.jpg", "species": "Cat", "name": "Milo",    "age": 2.5, "breed": "British Shorthair",   "description": "Color: Blue", "address": "789 Cat Avenue", "city": "Feline City", "phone_number": "555-321-098"},
            {"image": "dog1.jpg", "species": "Dog", "name": "Barry",   "age": 3,   "breed": "Bernese Mountain Dog","description": "Color: Tricolor", "address": "321 Dog Lane", "city": "Barksville", "phone_number": "555-654-321"},
            {"image": "dog2.jpg", "species": "Dog", "name": "Bella",   "age": 3.5, "breed": "Golden Retriever",    "description": "Color: Light Golden", "address": "654 Dog Street", "city": "Woofington", "phone_number": "555-456-789"},
            {"image": "dog3.jpg", "species": "Dog", "name": "Rocky",   "age": 4,   "breed": "German Shepherd",      "description": "Color: Black and Tan", "address": "987 Dog Avenue", "city": "Dogtown", "phone_number": "555-789-012"},
        ]
        for info in pets_info:
            url = f'images/{info["image"]}'
            if not Pet.query.filter_by(image_url=url).first():
                pet = Pet(
                    name=info["name"],
                    species=info["species"],
                    breed=info["breed"],
                    age=info["age"],
                    description=info["description"],
                    image_url=url,
                    address=info["address"],
                    city=info["city"],
                    phone_number=info["phone_number"]
                )
                db.session.add(pet)
                print(f"Added Pet: {pet.name} ({info['species']}) with image {url}")
        db.session.commit()
        print("Database seeding complete.")

if __name__ == '__main__':
    main()
    