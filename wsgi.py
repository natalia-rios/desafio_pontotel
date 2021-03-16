from project.main import main
from project import create_app, db

if __name__ == '__main__':
    db.create_all(app=create_app())
    app = create_app()
    app.run()
else:
    db.create_all(app=create_app())
    app = create_app()