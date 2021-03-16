import os
import unittest
 
from project import create_app, db, mail
 
TEST_DB = 'test.db'
 
class BasicTests(unittest.TestCase):
 
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
 
        mail.init_app(app)
        self.assertEqual(app.debug, False)
 
    def tearDown(self):
        pass
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def register(self, email, password):
        return self.app.post(
            '/signup',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_registration_duplicate_email(self):
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsReallyAwesome')
        self.assertIn(b'Endereco de email ja existe.', response.data)

    def test_invalid_login(self):
        response = self.login('patkenedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Seu email, PIS ou CPF esta incorreto ou nao esta cadastrado. Digite as informacoes corretamente.', response.data)
    
if __name__ == "__main__":
    unittest.main()