import hmac
import hashlib
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status as http

from fota.errors import SignatureValidationError
from cars.models import Car
from cars.serializers import CarSerializer
from main.models import Firmware

logger = logging.getLogger(__name__)

WEBHOOK_KEY = settings.WEBHOOK_KEY
UPGRADE_STATUS = "upgrade_status"
DOWNGRADE_STATUS = "downgrade_status"
REPORT = "report"


def validate_signature(payload: dict, received_signature: str, secret_key: str) -> bool:
    if not received_signature:
        return False

    hash_algorithm = hashlib.sha256
    required_string = ""
    for key in sorted(payload, key=str.lower):
        if payload[key] in [None, "null"]:
            payload[key] = ""
        x = "{key}={value},".format(key=key, value=payload[key])
        required_string = required_string + x

    expected_signature = hmac.new(
        WEBHOOK_KEY, required_string, hash_algorithm).hexdigest()
    print(expected_signature)
    print(received_signature)

    valid = hmac.compare_digest(expected_signature, received_signature)
    return valid


@csrf_exempt
def handle_webhook(request: WSGIRequest):
    received_signature = request.headers.get("signature")
    if not received_signature:
        return Response(data={"message": "Error! HMAC signature header not found!"}, status=http.HTTP_400_BAD_REQUEST)
    try:
        payload = json.loads(request.body.decode("utf-8"))
        is_valid = validate_signature(payload, received_signature, WEBHOOK_KEY)
        if is_valid:
            webhook_handlers = {
                UPGRADE_STATUS: firmware_upgrade,
                DOWNGRADE_STATUS: firmware_downgrade,
                REPORT: report
            }
            if payload["type"] in webhook_handlers.keys():
                logger.debug(
                    "Handling new webhook event of type: " + payload["type"])
                webhook_handlers[payload["type"]](payload=payload)
        raise SignatureValidationError
    except ValueError as e:
        return Response(data={"message": "An error occured while handling the payload!", "detail": e.__str__})
    except SignatureValidationError as e:
        return Response(data={"message": "An error occured while handling the payload!", "detail": e.message})


def firmware_upgrade(payload):
    status = payload["status"]
    print(status)
    if status == "success":
        car_id = payload.get("car_id")
        firmware_id = payload.get("firmware_id")
        try:
            car = Car.objects.get(pk=int(car_id))
            firmware = Firmware.objects.get(pk=int(firmware_id))
            car.installed_firmware = firmware
            car.save()
            car_item = CarSerializer(car)
            return Response(data={"status": "success", "car": car_item.data}, status=http.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={"status": "error",
                                  "details": "Couldn't complete operation!, Either the car object or the firmware object doesn't exist",},
                            status=http.HTTP_400_BAD_REQUEST)


def firmware_downgrade(payload):
    pass


def report(payload):
    pass
