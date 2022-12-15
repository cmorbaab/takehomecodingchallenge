import requests
from typing import List, Tuple
from custom_exception import InvalidGeoJSONException, InvalidClinicianIDException, InvalidStatusAPIResponseException

class ClinicianStatusAPIInterface:

    def __init__(self):
        self.BASE_URL = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"

    def get_clinician_status(self, clinician_id: int) -> Tuple[List[float], List[List[List[float]]]]:
        response = requests.get("{0}/clinicianstatus/{1}".format(self.BASE_URL, clinician_id))
        response.raise_for_status()
        
        response_json = response.json()
        # handle api errors
        if 'error' in response_json.keys():
            if response_json['error'] == "Invalid clinicianID":
                raise InvalidClinicianIDException(message="Clinician status API responded with error: 'Invalid clinicianID'. clinicianID = {0}".format(clinician_id))
            else:
                raise InvalidStatusAPIResponseException(message="Clinician status API responded with an error.")

        clinician_coordinates = self._get_clinician_coordinates(response_json)
        zone_coordinates = self._get_zone_coordinates(response_json)

        return clinician_coordinates, zone_coordinates



    def _get_clinician_coordinates(self, response: requests.Response) -> List[float]:
        num_point_features_found = 0
        clinician_coordinates = None
        for feature in response['features']:
            geometry = feature['geometry']
            if geometry['type'] == "Point":
                clinician_coordinates = geometry['coordinates']
                num_point_features_found += 1

        if (num_point_features_found != 1):
            raise InvalidGeoJSONException(message="Invalid GeoJSON data. Expected 1 point object to be found. Got {0} point object(s).".format(num_point_features_found))

        return clinician_coordinates
        

    def _get_zone_coordinates(self, response: requests.Response) -> List[List[List[float]]]:
        zone_coordinates = []
        for feature in response['features']:
            geometry = feature['geometry']
            if geometry['type'] == "Polygon":
                zone_coordinates += geometry['coordinates']
        
        return zone_coordinates