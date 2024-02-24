from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and phone are the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, phone, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        if not phone:
            raise ValueError(_("The Phone must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, phone, password, **extra_fields)


def photo_path(instance, filename):
    return "users/{0}/{1}".format(instance.id, filename)


class CustomUser(AbstractUser):
    username = None
    phone_validator = RegexValidator(
        r'^(01\d{9}|\+201\d{9})$', 'This is not a valid egyptian phone number')
    
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(
        _("phone number"), max_length=13, unique=True, validators=[phone_validator])
    photo = models.ImageField(upload_to=photo_path, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name() or self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
