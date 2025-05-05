import os
from app import create_app, db
from app.models import Pet, User
from werkzeug.security import generate_password_hash

def main():
    app = create_app()
    with app.app_context():
        # Reset database tables
        db.drop_all()
        db.create_all()
        # Create default admin user with known password
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('password', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            print("Created admin user 'admin' with password 'password'.")

        # Seed Pet records for each image
        img_dir = os.path.join(app.static_folder, 'images')
        images = sorted(f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)))
        for img in images:
            url = f'images/{img}'
            if not Pet.query.filter_by(image_url=url).first():
                name = os.path.splitext(img)[0]
                species = 'Dog' if name.lower().startswith('dog') else 'Cat'
                pet = Pet(
                    name=name.capitalize(),
                    species=species,
                    breed='Mixed',
                    age=2,
                    description=f'A friendly {species.lower()} named {name}.',
                    image_url=url
                )
                db.session.add(pet)
                print(f"Added Pet: {pet.name} ({species}) with image {url}")
        db.session.commit()
        print("Database seeding complete.")

if __name__ == '__main__':
    main()