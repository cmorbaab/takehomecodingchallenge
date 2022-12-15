from typing import List
from shapely import Point
from enum import Enum


class ClinicianSafetyStatus(Enum):
    INSIDE_ZONE = 0
    OUTSIDE_ZONE = 1
    UNKNOWN = 2


class Phlebotomist:
    def __init__(self, id: int):
        self.id = id
        self.last_location = None
        self.safety_status = ClinicianSafetyStatus.UNKNOWN
    
    def update_location(self, coordinates: List[float]) -> None:
        # add input validation in future
        self.last_location = Point(coordinates)

    def set_safety_status(self, status: ClinicianSafetyStatus) -> None:
        self.safety_status = status
