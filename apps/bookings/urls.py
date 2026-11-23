from django.urls import path

from apps.bookings.views.booking import BookingCreateView, BookingCancelView    


urlpatterns = [
    path(
        "",
        BookingCreateView.as_view(),
        name="booking-create",
    ),

    path(
        "<int:pk>/cancel/",
        BookingCancelView.as_view(),
        name="booking-cancel",
    ),
]