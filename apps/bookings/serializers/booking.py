from rest_framework import serializers

from apps.bookings.models import Booking


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=150)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Title is required.")

        return value


class BookingResponseSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "room_id",
            "user_id",
            "title",
            "start_time",
            "end_time",
            "status",
        ]
        read_only_fields = fields