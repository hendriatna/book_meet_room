
from django.db import models
from django.db.models import F, Func, Q, Value

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeOperators,
)

from apps.common.models import AuditModel


class BookingStatus(models.TextChoices):
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"


class Booking(AuditModel):

    id = models.BigAutoField(primary_key=True)

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="bookings",
        db_column="room_id",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="bookings",
        db_column="user_id",
    )

    title = models.CharField(
        max_length=150,
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )

    class Meta:
        db_table = "bookings"

        ordering = ["start_time"]

        constraints = [
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="booking_end_after_start",
            ),

            ExclusionConstraint(
                name="booking_no_room_time_overlap",
                expressions=[
                    ("room", RangeOperators.EQUAL),
                    (
                        Func(
                            F("start_time"),
                            F("end_time"),
                            Value("[)"),
                            function="TSTZRANGE",
                            output_field=DateTimeRangeField(),
                        ),
                        RangeOperators.OVERLAPS,
                    ),
                ],
                condition=Q(status=BookingStatus.CONFIRMED),
            ),
        ]

        indexes = [
            models.Index(
                fields=["room", "start_time", "end_time", "status"],
                name="booking_room_time_idx",
            ),
        ]

    def __str__(self):
        return self.title
