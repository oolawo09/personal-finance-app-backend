# !flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app import make_public
from models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SERVER_NAME'] = 'x'
        """
        RuntimeError: Application was not able to create a URL adapter for
        request independent URL generation. You might be able to fix this by
        setting the SERVER_NAME config variable.
        """
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_public(self):
        debt = {
                'id': '0' # I onnly need the id to run this test
                }

        import pdb; pdb.set_trace()
        with app.app_context():
            debt_with_public_url = make_public(debt)

    def test_get_auth_token(self):
        pass

    def test_verify_passwor(self):
        pass

    def test_get_debts(self):
        pass

    def test_index(self):
        pass

    def test_create_debt(self):
        pass

    def test_update_debt(self):
        pass

if __name__ == '__main__':
    unittest.main()
