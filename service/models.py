from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class Service(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLETED = "COMPLETED", _("Completed")

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


