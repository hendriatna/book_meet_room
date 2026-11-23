from rest_framework import serializers

from apps.rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "capacity",
            "is_active",
            "created_date",
            "updated_date",
            "created_by",
            "updated_by",
        ]

        read_only_fields = [
            "id",
            "created_date",
            "updated_date",
            "created_by",
            "updated_by",
        ]

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Room capacity must be greater than zero."
            )

        return value