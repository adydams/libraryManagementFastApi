from sys import api_version
from ..geolocation_functions.longitude_latitude import get_location_details_from_ip_address
from fastapi import APIRouter

router = APIRouter(
    prefix = "/users_ip_location_details",
    tags=['users_ip_location_details']
)

@router.get("/users_location_details")
def location_details_using_ip():
    return get_location_details_from_ip_address()
     