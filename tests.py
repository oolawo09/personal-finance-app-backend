# !flask/bin/python
import os
import unittest

from app import app, db
from models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_public():
        pass

    def test_get_auth_token():
        pass

    def test_verify_passwor():
        pass

    def test_get_debts():
        pass

    def test_index():
        pass

    def test_create_debt():
        pass

    def test_update_debt():
        pass
