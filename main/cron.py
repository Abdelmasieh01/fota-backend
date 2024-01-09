import requests
from decouple import config

URL = config('RENDER_HOST') + '/ping'


def ping():
    requests.get(URL)
