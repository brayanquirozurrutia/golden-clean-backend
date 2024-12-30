from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User, Address


class Service(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")  # Client created the service
        ACCEPTED = "ACCEPTED", _("Accepted")  # Employee accepted the service
        ON_THE_WAY = "ON_THE_WAY", _("On the way")  # Employee is on the way to the address
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")  # Employee is working on the service
        COMPLETED = "COMPLETED", _("Completed") # Employee completed the service

    client = models.ForeignKey(
        User,
        related_name="services",
        on_delete=models.RESTRICT,
        limit_choices_to={"role": User.Role.CLIENT},
    )
    employee = models.ForeignKey(
        User,
        related_name="assignments",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": User.Role.EMPLOYEE},
    )
    address = models.ForeignKey(
        Address,
        related_name="services",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    description = models.TextField()
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Service for {self.client.username} by {self.employee.username if self.employee else 'Unassigned'} - {self.status}"


