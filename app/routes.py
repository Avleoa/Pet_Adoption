from flask import render_template, redirect, url_for, request, flash, session
from app import db
from app.models import User, Pet, AdoptionRequest, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/ping')
def ping():
    return 'pong'

@main.route('/')
def index():
    # Show first 6 available pets on home page
    pets = Pet.query.filter_by(is_adopted=False).limit(6).all()
    return render_template('index.html', pets=pets)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password != confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('main.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('main.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('main.register'))
        # Use PBKDF2-SHA256 to hash password for compatibility
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/animals')
def animals():
    return render_template('animals.html')

@main.route('/adoption')
def adoption():
    return render_template('adoption.html')

@main.route('/animal-care')
def animal_care():
    return render_template('animal_care.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/pets')
def pets():
    # List available pets, optionally filter by search query
    query = request.args.get('q', '')
    if query:
        pets_list = Pet.query.filter(
            Pet.is_adopted==False,
            or_(
                Pet.name.ilike(f"%{query}%"),
                Pet.species.ilike(f"%{query}%")
            )
        ).all()
    else:
        pets_list = Pet.query.filter_by(is_adopted=False).all()
    return render_template('pets.html', pets=pets_list)

@main.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_details.html', pet=pet)

@main.route('/adopt/<int:pet_id>', methods=['GET', 'POST'])
def adopt_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == 'POST':
        # Process form data here (save to DB or send email)
        flash(f'Your adoption application for {pet.name} has been submitted!', 'success')
        return redirect(url_for('main.pet_details', pet_id=pet.id))
    return render_template('adoption_application.html', pet=pet)