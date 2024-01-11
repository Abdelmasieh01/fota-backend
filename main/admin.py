from typing import Any
from django.contrib import admin
from .models import Firmware, FirmwareLine
import os
from django.conf import settings

# Register your models here.


class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        lines = obj.file.open('r').read().splitlines()
        # print(lines)
        line_objects = FirmwareLine.objects.filter(firmware=obj)
        if line_objects.count():
            print(line_objects.delete())

        counter = 0
        line_objects = []
        for line in lines:
            if line.strip():
                line_objects.append(FirmwareLine(
                    firmware=obj, number=counter, line=line))
                counter += 1

        FirmwareLine.objects.bulk_create(line_objects)


class FirmwareLineAdmin(admin.ModelAdmin):
    list_display = ['firmware_name', 'number']


admin.site.register(Firmware, FirmwareAdmin)
admin.site.register(FirmwareLine, FirmwareLineAdmin)
