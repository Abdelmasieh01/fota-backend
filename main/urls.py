from django.urls import path
from . import views
from . import webhooks

app_name = "main"

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path("firmware/", views.FirmwareListView.as_view(), name="firmware-list"),
    path("latest-car/<int:car_id>/", views.get_latest_car_firmware, name="latest-car-firmware"),
    path("latest-model/<str:full_model>/", views.get_latest_model_firmware, name="latest-model-firmware"),
    path("firmware-lines/", views.FirmwareLineListView.as_view(), name="firmware-line-list"),
    path("firmware-line/<int:firmware_id>/<int:number>/", views.get_firmware_line, name="firmware-line"),
    path("firmware/webhook/", webhooks.handle_webhook, name="webhooks"),
]
