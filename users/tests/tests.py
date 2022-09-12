from ..models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTestCase(APITestCase):
    """This class is used to test the user registration"""

    data = {
        "username": "hamdan",
        "password": "pass7890",
        "email": "hamdan@gmail.com",
        "first_name": "ABC",
        "last_name": "XYZ",
    }

    def test_register(self):
        """
        This method is specifically used to create a user and then checking
        if the user is created successfully
        """

        response = self.client.post("/register", RegisterTestCase.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_same_username(self):
        """
        This method is specifically used to create a user and then checking
        if we create a user with same username and email
        """

        response = self.client.post("/register", RegisterTestCase.data)
        response_again = self.client.post("/register", RegisterTestCase.data)
        self.assertEqual(response_again.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationTestCase(APITestCase):
    """
    This class is used to test the user authentication i.e
    checks if the user is being authenticated properly and client
    is receiving a token
    """

    password = "qwerty123"

    def setUp(self):
        """
        We are setting up a User in this method for our test Cases and loging it in
        the application
        """

        self.user = UserFactory()
        self.user.set_password(self.password)
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.client.force_login(self.user)

    def test_authentication(self):
        """
        This method is testing the authentication api to test if the api is
        working correctly
        """

        data = {"username": self.user.username, "password": self.password}
        response = self.client.post("/login", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authentication_bad(self):
        data = {"username": "No_exist", "password": self.password}
        response = self.client.post("/login", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
