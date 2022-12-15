
class InvalidGeoJSONException(Exception):
    def __init__(self, message):            
        super().__init__(message)

class InvalidClinicianIDException(Exception):
    def __init__(self, message):            
        super().__init__(message)

class InvalidStatusAPIResponseException(Exception):
    def __init__(self, message):            
        super().__init__(message)