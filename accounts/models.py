from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You missed to enter the username")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_ADMIN = "admin"
    ROLE_HR = "human_resource"
    ROLE_TEAMLEAD = "teamlead"
    ROLE_DEVELOPER = "developer"
    ROLE_CHOICES = (
        ("", "No role"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_HR, "HR"),
        (ROLE_TEAMLEAD, "Teamlead"),
        (ROLE_DEVELOPER, "Developer"),
    )
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=10, blank=True)
    first_name = models.CharField(_("first name"), max_length=30)
    middle_name = models.CharField(_("middle name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=16, blank=True)
    country = models.CharField(_("countery"), max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default="")
    total_leaves = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    remaining_leaves = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(AbstractBaseUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        if old and old.role != self.role:  # Field role has changed
            self.resend_drip_messages = True

        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.email)
