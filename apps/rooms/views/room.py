from rest_framework import viewsets

from apps.rooms.models import Room
from apps.rooms.permissions.room import IsAdminOrReadOnly
from apps.rooms.serializers.room import RoomSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


    @action(
        detail=False,          # False jika untuk cek semua ruangan (/available/), True jika butuh ID (/{id}/available/)
        methods=["get"],      # Atau ["get"] jika hanya mengambil data tanpa mengubah status
        url_path="available",
    )
    def check_available(self, request):
        # Anda bisa memanggil self.get_queryset() di dalam sini
        queryset = self.get_queryset() 
        
        # Tambahkan logika pengecekan ketersediaan ruangan di sini
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = Room.objects.all()

        # ADMIN dapat melihat room aktif dan nonaktif.
        # USER hanya dapat melihat room aktif.
        if self.request.user.role != "ADMIN":
            queryset = queryset.filter(is_active=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user,
        )

    def perform_destroy(self, instance):
        # Soft delete agar histori booking tetap aman.
        instance.is_active = False
        instance.updated_by = self.request.user

        instance.save(
            update_fields=[
                "is_active",
                "updated_by",
                "updated_date",
            ]
        )