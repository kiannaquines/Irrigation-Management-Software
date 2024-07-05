from django.contrib import admin
from .models import User,FarmerLandInformation
from django.contrib.auth.admin import UserAdmin as OriginalAdmin

class CustomUserAdmin(OriginalAdmin):
    fieldsets = (
        *OriginalAdmin.fieldsets,
        (
            'User Information',
            {
                "fields" : (
                    "role",
                    "mobile",
                    "gender",
                    "address",
                ),
            }
        ),
    )

    add_fieldsets = (
        (None, 
        {
            'fields': ('username', 'password1', 'password2', 'email','role'),
        },
        ),
    )

    list_display = ("username","first_name","last_name","email","is_active","is_superuser",)
    search_fields = ("first_name","last_name","username",)

class FarmerLandInformationAdmin(admin.ModelAdmin):
    list_display = ("user","lot_number","hectares","square_meter","region",)
    list_filter = ("region","square_meter",)


admin.site.register(User,CustomUserAdmin)

admin.site.register(FarmerLandInformation,FarmerLandInformationAdmin)
