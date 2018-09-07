import json

from .entry import EntryClass

SIGNUP_URL = '/api/v1/auth/signup'
LOGIN_URL = '/api/v1/auth/login'


class TestAuth(EntryClass):
    """ Add tests for Auth """

    def test_user_registration(self):
        """ Test user registration works correcty """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "registration successful, now login")

    def test_user_wrong_registration(self):
        """Test wrong registration when user doesn't fill fields"""
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'danny', 'email': 'short@gmail.com', 'password': ''}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "All fields are required")

    def test_user_cannot_register_twice(self):
        """ Test User cannot register twice """
        self.client.post(SIGNUP_URL,
                         data=json.dumps(self.user_data), content_type='application/json')
        response2 = self.client.post(SIGNUP_URL,
                                     data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response2.status_code, 203)
        result = json.loads(response2.data.decode())
        self.assertEqual(result["message"], "User already exists")

    def test_user_cannot_register_with_short_password(self):
        """ Test User cannot register if password is less than 8 characters """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'dannyb', 'email': 'oti@gmail.com', 'password': 'pass'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Password should be atleast 8 characters")

    def test_user_cannot_register_with_short_username(self):
        """ Test user can register with username less than 4 charcters """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'dan', 'email': 'oti@gmail.com', 'password': 'pass12345'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Username should be atleast 4 characters")

    def test_user_cannot_register_with_wrong_email_format(self):
        """ Test user should not be able to register with invalid email """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': 'dannyb', 'email': 'danny@', 'password': 'pass254'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"], "Invalid email. Ensure email is of the form example@mail.com")

    def test_user_cannot_register_with_invalid_username(self):
        """ Test user should not be able to register with invalid username """
        response = self.client.post(SIGNUP_URL,
                                    data=json.dumps(
                                        {'username': '#_danny', 'email': 'danny@gmail.com', 'password': 'pass12345'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid username")

    def test_user_login(self):
        """ Test registered user should be able to login """
        self.test_user.save()
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'dannyb', 'password': 'pass12345'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You are successfully logged in")

    def test_login_for_user_not_registered(self):
        """ Test login for Non registered user """
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'otieno', 'password': 'otieno254'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User unavailable')

    def test_wrong_password(self):
        """Test for authenication when password is wrong
        User should not be able to login
        """
        self.test_user.save()
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(
                                        {'username': 'dannyb', 'password': 'andela'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Username or password is wrong.')