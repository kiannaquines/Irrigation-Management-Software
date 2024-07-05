from django.contrib import admin
from main_app.models import Reservation,Payment,Operation,Equipment

admin.site.site_title = "Irrigators Assocation System"
admin.site.site_header = "Irrigators Assocation Information Management System"



class ReservationAdmin(admin.ModelAdmin):
    list_display = ("farmer","schedule","reservation_status","confirmation","date_added",)
    list_filter = ("date_added","reservation_status","equipment")

    add_fieldsets = (
        (None,
            {
                'fields': ('farmer', 'schedule', 'reservation_status',),
            }
        )
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reservation","payment_amount","balance","payment_type",)
    list_filter = ("payment_type",)

class OperationAdmin(admin.ModelAdmin):
    list_display = ("operation_name","operation_status","date_added",)
    list_filter = ("operation_status","date_added",)


# class EquipmentAdmin(admin.ModelAdmin):
#     list_display = ("equipment_name","equipment_status","date_added",)
#     list_filter = ("equipment_name","date_added",)


admin.site.register(Equipment)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Operation,OperationAdmin)