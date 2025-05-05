import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Add this line

db = SQLAlchemy()
migrate = Migrate()  # Add this line

def create_app():
    # Point templates to top-level `templates/` and serve static from app/static
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(project_root, 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config')
    db.init_app(app)
    migrate.init_app(app, db)  # Add this line

    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        from app import routes
        db.create_all()

    return app