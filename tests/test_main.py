import os
import unittest

from project import app,db
from project.models import User

basedir = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.db'


class MainTests(unittest.TestCase):

    def setUp(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper methods
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)


    def test_404_error(self):
        response = self.app.get('/This-route-does-not-exist')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry', response.data)

    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEquals(response.status_code, 200)

    # def test_500_error(self):
    #     bad_user = User(
    #         name='JeremyHunt',
    #         email='Jeremy@malpy.com',
    #         password='nosaltinourwounds'
    #     )
    #     db.session.add(bad_user)
    #     db.session.commit()
    #     response = self.login('JeremyHunt', 'nosaltinourwounds')
    #     self.assertEquals(response.status_code, 500)
    #     self.assertNotIn(b'ValueError: Invalid salt', response.data)
    #     self.assertIn(b'Something went terribly wrong.', response.data)