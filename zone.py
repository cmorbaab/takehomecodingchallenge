from typing import List
from shapely import Point, Polygon
from phlebotomist import Phlebotomist


class Zone:
    def __init__(self, coordinates_list: List[List[List[float]]]):
        # add input validation in future
        self.polygons = []
        for shape in coordinates_list:
            self.polygons.append(Polygon(shape))
    
    
    def contains(self, clinician: Phlebotomist) -> bool:
        for polygon in self.polygons:
            if clinician.last_location.within(polygon) or clinician.last_location.touches(polygon):
                return True
        
        return False
