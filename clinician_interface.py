from typing import List, Dict, Tuple
from zone import Zone
from phlebotomist import Phlebotomist, ClinicianSafetyStatus

class ClinicianInterface:
    def __init__(self, clinician_ids: List[int] = [], zones: Dict[int, Zone] = dict()):
        self.clinicians = dict() # clinician[id] --> clinician
        self.zones = zones # zones[clinician id] --> zone
        
        for id in clinician_ids:
            self.clinicians[id] = Phlebotomist(id=id)

    def get_clinician_ids(self) -> List[int]:
        return list(self.clinicians.keys())
    
    def update_clinician_location(self, clinician_id: int, clinician_coordinates: List[float]) -> None:
        clinician = self.clinicians[clinician_id]
        clinician.update_location(coordinates=clinician_coordinates)

    def update_zone(self, clinician_id: int, zone_coordinates: List[float]) -> None:
        self.zones[clinician_id] = Zone(zone_coordinates)
    
    def check_clinician_within_zone(self, clinician_id: int) -> Tuple[bool, bool]:
        clinician = self.clinicians[clinician_id]
        if clinician_id in self.zones:
                clinician_zone = self.zones[clinician_id]
                # if clinician is in the zone 
                if clinician_zone.contains(clinician):
                    new_broadcast = False # new broadcast means whether we will make a alert broadcast
                    clinician.set_safety_status(ClinicianSafetyStatus.INSIDE_ZONE)
                    return True, new_broadcast # within, new_broadcast
                else:
                    previous_status = clinician.safety_status
                    new_broadcast = previous_status != ClinicianSafetyStatus.OUTSIDE_ZONE
                    clinician.set_safety_status(ClinicianSafetyStatus.OUTSIDE_ZONE)
                    return False, new_broadcast # within, new_broadcast
