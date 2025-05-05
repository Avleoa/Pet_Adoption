import os
from app import create_app, db
from app.models import Pet

def main():
    app = create_app()
    with app.app_context():
        for pet in Pet.query.all():
            filename = os.path.basename(pet.image_url)
            new_url = f'images/{filename}'
            pet.image_url = new_url
            print(f"Pet {pet.id} ({pet.name}) image_url updated to {new_url}")
        db.session.commit()
        print("All pet image URLs normalized.")

if __name__ == '__main__':
    main()