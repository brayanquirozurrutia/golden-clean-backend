from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom User model
class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", _("Client")
        EMPLOYEE = "EMPLOYEE", _("Employee")

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )

# Region model
class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Comuna model
class Comuna(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name="comunas", on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name}, {self.region.name}"

# Address model
class Address(models.Model):
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    comuna = models.ForeignKey(Comuna, related_name="addresses", on_delete=models.RESTRICT)
    user = models.ForeignKey(
        User,
        related_name="addresses",
        on_delete=models.RESTRICT,
        limit_choices_to={"role": User.Role.CLIENT},
    )

    def __str__(self):
        return f"{self.street} {self.number}, {self.comuna.name}, {self.comuna.region.name}"
