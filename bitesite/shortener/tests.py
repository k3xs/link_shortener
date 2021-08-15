from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.test import TestCase

from .models import UserModel, Links, Feedback


class UserModelViewsTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_bob = UserModel.objects.create_user('bob', password='qwerty-123')
        self.user_eve = UserModel.objects.create_user('eve', password='qwerty-123')
        self.superuser = UserModel.objects.create_superuser('ann', password='qwerty-123')

    def tearDown(self) -> None:
        UserModel.objects.all().delete()
        super().tearDown()

    def test_user_login(self):
        login_url = reverse('login')
        self.client.logout()
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Checking that the login page is available to an anonymous user')

        self.client.force_login(self.user_bob)
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Checking that the login page is available to Bob')

    def test_login(self):
        login_url = reverse('login')
        self.client.logout()
        response = self.client.post(login_url, data={'username': 'bob', 'password': 'qwerty-123'})
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code, 'Checking the login')
        self.assertEqual(response.headers['location'], '/', 'Checking that the redirect is to the correct page')

        self.client.logout()
        response = self.client.post(login_url, data={'username': 'bob', 'password': 'qwerty-124'})
        self.assertEqual(response.status_code, HttpResponse.status_code, 'Checking if you entered an incorrect login/password')
        self.assertIn('Please enter a correct username and password. Note that both fields may be case-sensitive.', response.content.decode())

    def test_logout(self):
        logout_url = reverse('logout')
        redirect_url = reverse('login')
        self.client.force_login(self.user_bob)
        self.assertIn('_auth_user_id', self.client.session, 'Checking that the user is logged in')

        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)

        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.headers['location'], redirect_url)
        self.assertNotIn('_auth_user_id', self.client.session, 'Checking that the user is logged in')

    def test_user_can_see_my_links_page(self):
        my_links_url = reverse('my_links')
        self.client.logout()
        response = self.client.get(my_links_url)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Checking that the link list page is not accessible to an anonymous user')

        self.client.force_login(self.user_bob)
        response = self.client.get(my_links_url)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Checking that the link list page is available to the logged in user')

        self.client.force_login(self.user_eve)
        response = self.client.get(my_links_url)
        self.assertIn('', response.content.decode(), 'Checking that the user sees only their own links')

    def test_user_create_short_link(self):
        create_short_link = reverse('create_short_link')
        self.client.logout()
        response = self.client.get(create_short_link)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code,
                         'Checking that the page for creating short links is not accessible to an anonymous user')

        self.client.force_login(self.user_bob)
        response = self.client.get(create_short_link)
        self.assertEqual(response.status_code, HttpResponse.status_code,
                         'Checking that the page for creating short links is available to the logged in user')


class LinksModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user_bob = UserModel.objects.create_user('bob', password='qwerty-123')
        self.link = Links.objects.create(
            user=self.user_bob,
            original_url='https://docs.python.org/3/library/functions.html#abs',
            shorten_url='abs',
        )

    def tearDown(self):
        Links.objects.all().delete()
        UserModel.objects.all().delete()
        super().tearDown()

    def test_short_link_create(self):
        link = Links.objects.get(id=self.link.id)
        self.assertEqual(link.original_url, 'https://docs.python.org/3/library/functions.html#abs', 'Checking the name of the original link')
        self.assertEqual(link.shorten_url, 'abs', 'Checking the name of a short link')

    def test_link_edit(self):
        link = Links.objects.get(id=self.link.id)
        link.shorten_url = 'abs()'
        link.save()
        link = Links.objects.get(id=self.link.id)
        self.assertEqual(link.shorten_url, 'abs()', 'Checks for saving changes after editing')

    def test_link_delete(self):
        link = Links.objects.get(id=self.link.id)
        link.delete()
        with self.assertRaises(Links.DoesNotExist):
            Links.objects.get(id=self.link.id)

class FeedbackModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.feedback = Feedback.objects.create(
            sender='user@localhost.com',
            message='hello world!!!',
        )

    def tearDown(self):
        Feedback.objects.all().delete()
        super().tearDown()

    def test_feedback_create(self):
        feedback = Feedback.objects.get(id=self.feedback.id)
        self.assertEqual(feedback.sender, 'user@localhost.com', 'Checking the name of sender')
        self.assertEqual(feedback.message, 'hello world!!!', 'Checking the message')

class UserModelModelTestCase(TestCase):


    def test_create(self):
        user = UserModel.objects.create_user('bob', password='123')
        self.assertEqual(user.username, 'bob', 'Checking the username')