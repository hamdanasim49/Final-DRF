from faker import Factory
from rest_framework import status

from .factory import NoteFactory
from users.models import User
from users.tests.tests import AuthenticationTestCase

faker = Factory.create()


class NotesCrudTestCase(AuthenticationTestCase):
    """This class is used to test the notes CRUD operations which are created
    by ModelViewset"""

    url = "/notes/"

    def setUp(self):
        super().setUp()
        self.note = NoteFactory(user=self.user)
        self.note.save()
        self.data = {
            "username": "unknown",
            "password": "pass7890",
        }

        self.data1 = {
            "username": "unknown",
            "password": "pass7890",
            "email": "unknown@gmail.com",
            "first_name": "ABC",
            "last_name": "XYZ",
        }

        User.objects.create(
            username=faker.profile(fields=["username"])["username"],
            password=faker.password(),
            email=faker.email(),
        )

    def test_create_note(self):
        """
        This is a test for create_note api.
        It is checking if the note ie being created correctly.
        """

        data = {"title": faker.name(), "text": faker.text()}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["text"], data["text"])

    def test_create_note_failure(self):
        """
        This test is used to ensure that wrong data passed to the create api doesn't
        create the note object. For the test we are not passing the title field in the data
        """

        data = {"text": faker.text()}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["title"][0].title(), "This Field Is Required.")

    def test_list_note(self):
        """
        This test is used to check Retrieve Note for a User Api.
        If notes are being listed correctly the test should return 200 ok status code with the listed notes
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note(self):
        """
        This test is used to check when we retrieve data of a particular note with
        an ID
        """

        response = self.client.get("/notes/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.note.title)
        self.assertEqual(response.data["text"], self.note.text)

    def test_get_note_failure(self):
        """
        This test is used to check when we retrieve data of a particular note with
        an ID
        """

        response = self.client.get("/notes/5/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"].title(), "Not Found.")

    def test_delete_note(self):
        """This test is used to check the delete note api"""

        response = self.client.delete("/notes/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_note_failure(self):
        """This test is for checking if delete a note that does not exist"""

        response = self.client.delete("/notes/5/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"].title(), "Not Found.")

    def test_update_note(self):
        """
        test for: update_note api
        purpose: checks if the data is correctly updated by the api
        """
        data = {"title": "updated data", "text": "the data is updated"}
        response = self.client.patch("/notes/1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note_failure(self):
        """
        test for: update_note api
        purpose: checks if the data is updated for a specific note correctly
        """
        data = {"title": faker.text(), "text": faker.text()}
        response = self.client.patch(
            "/notes/25/", data=data
        )  # The note_id passed in the url is incorrect
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"].title(), "Not Found.")

    def test_shared_to(self):
        """
        This test is used to check if we try to share a note with a user that
        do exist. if a user exists it will return 200 OK
        """

        shared_with = {"shared_with": "2"}
        response = self.client.patch("/notes/1/", data=shared_with)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shared_to_failure(self):
        """
        This test is used to check if we try to share a note with a user that
        does not exist. if a user does not exist it will returnn 400 failure request error
        """

        shared_with = {"shared_with": "4"}
        response = self.client.patch("/notes/1/", data=shared_with)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_comment(self):
        """
        This test is the positive test for adding a comment to a note,
        it will return 200 OK if the note exists
        """

        body = {"note": "1", "text": faker.text()}
        response = self.client.post("/comments/", data=body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_failure(self):
        """
        This test is the negative test for adding a comment to a note that
        does not exist, it will return 400 failure if the note exists
        """

        body = {"note": "3", "text": faker.text()}
        response = self.client.post("/comments/", data=body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comment(self):
        """
        This test is the good case test for getting comments for a note
        """

        self.test_add_comment()
        response = self.client.get("/notes/1/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
