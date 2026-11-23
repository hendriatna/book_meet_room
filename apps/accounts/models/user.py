
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.accounts.managers.user_manager import UserManager
from apps.common.models import AuditModel


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Administrator"
    USER = "USER", "Regular User"


class User(AuditModel, AbstractBaseUser):

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        max_length=150,
        unique=True,
    )

    # Django menggunakan field password secara internal.
    # Nama kolom database mengikuti spesifikasi soal.
    password = models.CharField(
        max_length=255,
        db_column="password_hash",
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    # AbstractBaseUser menyediakan last_login secara default.
    # Kita hilangkan karena tidak termasuk spesifikasi tabel.
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "users"
        ordering = ["-created_date"]

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return self.role == UserRole.ADMIN

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
