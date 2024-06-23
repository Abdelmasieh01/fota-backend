from django.contrib import admin
from .models import Car, CarModel, CarReport, CarClass, CarColor
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display = ["model", "owner", "registration_date"]
    readonly_fields = ["registration_date"]


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "year"]


class CarReportAdmin(admin.ModelAdmin):
    list_display = ["car", "timestamp"]
    ordering = ["-timestamp"]


class CarColorAdmin(admin.ModelAdmin):
    list_display = ["name", "hex_code"]


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarReport, CarReportAdmin)
admin.site.register(CarColor, CarColorAdmin)
admin.site.register(CarClass)
