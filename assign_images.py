import os
from app import create_app, db
from app.models import Pet

def main():
    app = create_app()
    with app.app_context():
        img_dir = os.path.join(app.static_folder, 'images')
        # List and sort image filenames
        images = sorted(f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)))
        pets = Pet.query.filter_by(is_adopted=False).order_by(Pet.id).all()
        for pet, img in zip(pets, images):
            pet.image_url = f'images/{img}'
            print(f"Assigned {img} to pet id={pet.id} name={pet.name}")
        db.session.commit()
        print("Image assignment complete.")

if __name__ == '__main__':
    main()