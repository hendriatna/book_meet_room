from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.bookings.exceptions import (
    InvalidBookingTime,
    RoomConflict,
    RoomInactive,
    RoomNotFound,
    BookingNotFound,
    BookingAlreadyCancelled
)
from apps.bookings.models import Booking, BookingStatus
from apps.rooms.models import Room


def create_booking(
    *,
    room_id: int,
    user,
    title: str,
    start_time,
    end_time,
):
    # Validasi waktu.
    if end_time <= start_time:
        raise InvalidBookingTime(
            "end_time must be greater than start_time."
        )

    if start_time < timezone.now():
        raise InvalidBookingTime(
            "start_time cannot be in the past."
        )

    try:
        with transaction.atomic():

            # Lock baris room agar request booking lain
            # untuk room yang sama harus menunggu.
            try:
                room = Room.objects.select_for_update().get(
                    id=room_id
                )
            except Room.DoesNotExist:
                raise BookingNotFound()

            if not room.is_active:
                raise RoomInactive()

            # Cek overlap hanya pada booking CONFIRMED.
            has_conflict = Booking.objects.filter(
                room=room,
                status=BookingStatus.CONFIRMED,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if has_conflict:
                raise RoomConflict()

            # Simpan booking.
            booking = Booking.objects.create(
                room=room,
                user=user,
                title=title,
                start_time=start_time,
                end_time=end_time,
                status=BookingStatus.CONFIRMED,
                created_by=user,
                updated_by=user,
            )

            return booking

    except IntegrityError:
        # Perlindungan tambahan dari constraint database,
        # termasuk jika terjadi konflik yang tidak terdeteksi
        # oleh pengecekan aplikasi.
        raise RoomConflict()


def cancel_booking(*, booking_id: int, user):
    with transaction.atomic():

        try:
            booking = (
                Booking.objects
                .select_for_update()
                .select_related("room", "user")
                .get(id=booking_id)
            )
        except Booking.DoesNotExist:
            raise BookingNotFound()

        # USER hanya dapat membatalkan booking miliknya.
        if user.role != "ADMIN" and booking.user_id != user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You are not allowed to cancel this booking."
            )

        if booking.status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelled()

        booking.status = BookingStatus.CANCELLED
        booking.updated_by = user

        booking.save(
            update_fields=[
                "status",
                "updated_by",
                "updated_date",
            ]
        )

        return booking