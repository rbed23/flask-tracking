from json import loads
from re import compile, VERBOSE
import requests

FREE_GEOIP_URL = "http://freegeoip.net/json/{}"
VALID_IP = compile(r"""
\b
(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\b
""", VERBOSE)


def get_geodata(ip):
    """
    Search for geolocation information using http://freegeoip.net/
    """
    if not VALID_IP.match(ip):
        raise ValueError('Invalid IPv4 format')

    url = FREE_GEOIP_URL.format(ip)
    data = {}

    try:
        response = requests.get(url)
        data = response.json()
    except Exception:
        pass

    return data
