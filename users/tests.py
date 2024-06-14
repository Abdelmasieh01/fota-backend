from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@fota.com", phone="010000000", password="123")
        self.assertEqual(user.email, "test@fota.com")
        self.assertEqual(user.phone, "010000000")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="", phone="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", phone="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@fota.com", phone="010000000", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.phone, "010000000")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", phone="010000000", password="foo", is_superuser=False)
        


class UserTestCase(TestCase):
    pass