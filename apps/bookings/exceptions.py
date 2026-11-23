from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidBookingTime(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "INVALID_TIME"
    default_detail = "Invalid booking time."

    def __init__(self, detail=None):
        super().__init__(
            detail={
                "error_code": "INVALID_TIME",
                "message": detail or self.default_detail,
            }
        )


class RoomNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "ROOM_NOT_FOUND"
    default_detail = "Room not found."

    def __init__(self):
        super().__init__(
            detail={
                "error_code": "ROOM_NOT_FOUND",
                "message": self.default_detail,
            }
        )


class RoomInactive(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "ROOM_INACTIVE"
    default_detail = "Room is not active."

    def __init__(self):
        super().__init__(
            detail={
                "error_code": "ROOM_INACTIVE",
                "message": self.default_detail,
            }
        )


class RoomConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "ROOM_CONFLICT"
    default_detail = "Room already has a confirmed booking in this time range."

    def __init__(self):
        super().__init__(
            detail={
                "error_code": "ROOM_CONFLICT",
                "message": self.default_detail,
            }
        )


class BookingAlreadyCancelled(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "BOOKING_ALREADY_CANCELLED"

    def __init__(self):
        super().__init__(
            detail={
                "error_code": "BOOKING_ALREADY_CANCELLED",
                "message": "Booking has already been cancelled.",
            }
        )


class BookingNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "BOOKING_NOT_FOUND"

    def __init__(self):
        super().__init__(
            detail={
                "error_code": "BOOKING_NOT_FOUND",
                "message": "Booking not found.",
            }
        )