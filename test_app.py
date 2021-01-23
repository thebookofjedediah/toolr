from app import app
from unittest import TestCase
from flask import session

class HomeViewTestCase(TestCase):
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="h3 mb-5">Stop buying tools.</h2>', html)

class LoginRegisterViewTestCase(TestCase):
    def test_register_page(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-1">Sign Up</h1>', html)

    # def test_register_post_page(self):
    #     with app.test_client() as client:
    #         res = client.post('/register', follow_redirects=True, data={
    #             'username': 'marnold',
    #             'password': 'password', 
    #             'email': 'harnold@gmail.com', 
    #             'first_name': 'Hed',
    #             'last_name': 'Arnold',
    #             'zip_code': 43952
    #         })
    #         html = res.get_data(as_text=True)
    #         print("Here is the html", html)
    #         self.assertEqual(res.status_code, 200)
    
    def test_login_page(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-1">Sign In</h1>', html)