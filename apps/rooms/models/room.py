
from django.db import models

from apps.common.models import AuditModel


class Room(AuditModel):

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "rooms"
        ordering = ["name"]

    def __str__(self):
        return self.name
