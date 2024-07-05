from django.urls import path
from farmer_portal import views

urlpatterns = [
    path("balances/",views.view_balances,name="balances"),
    path("add_reservation/",views.add_reservation,name="add_my_reservation"),
    path("available_equipments/",views.equipment_view,name="available_equipments"),
    path("update_reservation/<int:pk>",views.UpdateReservationView.as_view(),name="update_my_reservation"),
    path("delete_my_reservation/<int:pk>",views.DeleteReservationView.as_view(),name="delete_my_reservation"),
    path("cancel_reservation/<int:pk>",views.cancel_reservation,name="cancel_reservation"),
    path("my_reservations/",views.reservations,name="my_reservations"),
    path("my_profile/<int:pk>",views.UpdateFarmerLandInformationView.as_view(),name="my_profile"),
    path("my_profileinfo/<int:pk>",views.UpdateFarmerInfoView.as_view(),name="my_profileinfo"),
]