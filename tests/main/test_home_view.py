from flask_testing import TestCase
from app import create_app

class TestHomeView(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_home(self):
        response = self.client.get('/hello')
        text = response.data.decode()
        print(text)
        self.assertIn('Goodbye', text)
