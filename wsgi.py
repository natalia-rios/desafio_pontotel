from project.main import main
from project import create_app, db

if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    app = create_app()