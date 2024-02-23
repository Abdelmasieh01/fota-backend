from rest_framework import serializers
from .models import Firmware, FirmwareLine

class FirmwareSerializer(serializers.ModelField):
    lines_count = serializers.SerializerMethodField()

    def get_lines_count(self, obj):
        count = FirmwareLine.objects.filter(firmware=obj).count()
        return count

    class Meta:
        model = Firmware
        fields = ('name', 'version', 'file', 'lines_count', 'car_model')
    
class FirmwareLineSerializer(serializers.Serializer):
    class Meta:
        model = FirmwareLine
        fields = ('firmware_name', 'number', 'line')