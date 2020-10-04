import requests
import datetime
from functools import wraps
from flask import request
from api import settings
from database import db_instance


def whitelisted(f):
    """Ensure that the request's IP to the API is in the whitelist"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip_address = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        if js["status"] != "fail":
            country = js["countryCode"]
            if country not in settings.WHITELIST:
                db_instance.add_black_ip(ip_address, datetime.datetime.now())
                return None, 403

        return f(*args, **kwargs)

    return decorated_function