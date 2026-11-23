from rest_framework.routers import DefaultRouter

from apps.rooms.views.room import RoomViewSet


router = DefaultRouter()

router.register(
    r"",
    RoomViewSet,
    basename="room",
)

urlpatterns = router.urls