cd /Users/aleksandra/myproject
source pet_project/bin/activate
python run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)