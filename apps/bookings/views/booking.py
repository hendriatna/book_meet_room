from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookings.serializers.booking import (
    BookingCreateSerializer,
    BookingResponseSerializer,
)
from apps.bookings.services.booking_service import create_booking, cancel_booking


class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = create_booking(
            room_id=serializer.validated_data["room_id"],
            user=request.user,
            title=serializer.validated_data["title"],
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
        )

        response_serializer = BookingResponseSerializer(booking)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        booking = cancel_booking(
            booking_id=pk,
            user=request.user,
        )

        serializer = BookingResponseSerializer(booking)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )