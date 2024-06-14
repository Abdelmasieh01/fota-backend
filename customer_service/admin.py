from django.contrib import admin
from .models import Queue

# Register your models here.
class QueueAdmin(admin.ModelAdmin):
    list_display = ["user", "timestamp"]
    
admin.site.register(Queue, QueueAdmin)