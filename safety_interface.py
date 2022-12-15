from email_interface import EmailInterface
from clinician_status_api_interface import ClinicianStatusAPIInterface
from clinician_interface import ClinicianInterface
import datetime
from typing import List
from custom_exception import InvalidGeoJSONException , InvalidStatusAPIResponseException, InvalidClinicianIDException
from requests.exceptions import HTTPError

class SafetyInterface:
    def __init__(self, clinician_ids: List[int]):
        self.clinicianInterface = ClinicianInterface(clinician_ids=clinician_ids)
        self.clinicianStatusAPIInterface = ClinicianStatusAPIInterface()
        self.emailInterface = EmailInterface()
        self.email_receiver = "coding-challenges+alerts@sprinterhealth.com" 

    def verify_safety(self) -> None:
        for id in self.clinicianInterface.get_clinician_ids():
            try:
                clinician_coordinates, zone_coordinates = self.clinicianStatusAPIInterface.get_clinician_status(clinician_id=id)
                
                self.clinicianInterface.update_clinician_location(clinician_id=id, clinician_coordinates=clinician_coordinates)
                self.clinicianInterface.update_zone(clinician_id=id, zone_coordinates=zone_coordinates)
                
                within, new_broadcast = self.clinicianInterface.check_clinician_within_zone(clinician_id=id)
                if (not within and new_broadcast): # if outside and we need to broadcast
                    print("Alert - clinician {} is outside safety zone".format(id)) # TODO use logging system here
                    self._alert_clinician_outside_zone(clinician_id=id)

            # handle exceptions raised from clinicianStatusAPIInterface.get_clinician_status
            except (InvalidGeoJSONException, InvalidClinicianIDException) as e:
                print(str(e)) # TODO use logging system here
            except (HTTPError,InvalidStatusAPIResponseException) as e:
                # api did not respond --> alert
                print(str(e)) # TODO use logging system here
                self._alert_clinician_outside_zone(clinician_id=id)
                continue 
            


    
    def _alert_clinician_outside_zone(self, clinician_id: int) -> None:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')# local time zone
        subject = "Alert (Cameron Baab): Clinician {0} Outside of Safety Zone".format(clinician_id)
        body = "Clinician {0} was detected to be outside of the safety zone at the following time: {1}".format(clinician_id, current_time)

        self.emailInterface.send_email(email_receiver=self.email_receiver, subject=subject, body=body)