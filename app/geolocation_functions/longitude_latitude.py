import socket
from urllib.request import urlopen, urlretrieve 
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



def get_ip2():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return local_ip


def get_location_details_from_ip_address():
    with urlopen("https://geolocation-db.com/jsonp/{get_ip}") as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")
        return data
        