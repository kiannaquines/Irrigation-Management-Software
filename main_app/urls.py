from django.urls import path
from .views import DashboardView,PaymentView,ReservationView,OperationView,AddOperation,AddReservation,AddPayment,UpdateOperation,UpdatePayment,UpdateReservation,DeleteOperation,DeletePayment,DeleteReservation,AddUserView,FarmerView,UpdateUserView,DeleteUserView,UpdateProfileView,EquipmentView,AddEquipmentView,UpdateEquipmentView,DeleteEquipmentView,generate_reports_view,generate_reports_filter_by_date_view,activate_account,map_view,ReportView,change_payment_value

urlpatterns = [
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
    path("payment/",PaymentView.as_view(),name="payment"),
    path("reservation/",ReservationView.as_view(),name="reservation"),
    path("operation/",OperationView.as_view(),name="operation"),
    path("users/",FarmerView.as_view(),name="farmer"),
    path("equipment/", EquipmentView.as_view(),name="equipment"),

    path("map/",map_view,name="map"),
    path("report/",ReportView.as_view(),name="report"),

    path("add_operation/",AddOperation.as_view(),name="add_operation"),
    path("add_payment/",AddPayment.as_view(),name="add_payment"),
    path("add_reservation/",AddReservation.as_view(),name="add_reservation"),
    path("add_user/",AddUserView.as_view(),name="add_user"),
    path("add_equipment/",AddEquipmentView.as_view(),name="add_equipment"),

    path("edit_operation/<int:pk>",UpdateOperation.as_view(),name="edit_operation"),
    path("edit_payment/<int:pk>",UpdatePayment.as_view(),name="edit_payment"),
    path("edit_reservation/<int:pk>",UpdateReservation.as_view(),name="edit_reservation"),
    path("edit_user/<int:pk>",UpdateUserView.as_view(),name="edit_user"),
    path("edit_equipment/<int:pk>",UpdateEquipmentView.as_view(),name="edit_equipment"),

    path("delete_operation/<int:pk>",DeleteOperation.as_view(),name="delete_operation"),
    path("delete_payment/<int:pk>",DeletePayment.as_view(),name="delete_payment"),
    path("delete_reservation/<int:pk>",DeleteReservation.as_view(),name="delete_reservation"),
    path("delete_user/<int:pk>",DeleteUserView.as_view(),name="delete_user"),
    path("delete_equipment/<int:pk>",DeleteEquipmentView.as_view(),name="delete_equipment"),


    path("update_profile/<int:pk>",UpdateProfileView.as_view(),name="update_profile"),

    path("generate_report_by_date/",generate_reports_filter_by_date_view,name="generate_report_by_date"),
    path('generate_report_view/',generate_reports_view,name='generate_reports_view'),
    path('activate_account/<int:pk>',activate_account,name='activate_account'),

    path("change_payment_value/", change_payment_value,name="change_payment_value"),
]