import pytest
from phlebotomist import Phlebotomist
from zone import Zone
import requests
import requests_mock
import json
from email_interface import EmailInterface
from clinician_status_api_interface import ClinicianStatusAPIInterface
from clinician_interface import ClinicianInterface

"""
Testing
    - Zone, Person
        - inside zone
        - on line
        - outside zone
        - outside - weird shape 
    - API
        - bad json data
        - bad response 
        - double broadcast
        - bad clinician ids 
        - normal
    Main
        - no ids 

"""

@pytest.fixture
def clinicianWithinA():
    clinician = Phlebotomist(id=0)
    clinician.update_location(coordinates=[-121.93296432495117, 37.29139890536388])
    return clinician


@pytest.fixture
def clinicianOutsideA():
    clinician = Phlebotomist(id=0)
    clinician.update_location(coordinates=[-121.95096432495117, 37.29139890536388])
    return clinician
    
@pytest.fixture
def clinicianWithinB():
    clinician = Phlebotomist(id=1)
    clinician.update_location(coordinates=[-122.032871276338, 37.351075031997986])
    return clinician

@pytest.fixture
def clinicianOnLineB():
    clinician = Phlebotomist(id=1)
    clinician.update_location(coordinates=[-122.0328712463379, 37.351075031997986])
    return clinician

@pytest.fixture
def coordinatesWithinB():
    return [-122.032871276338, 37.351075031997986]

@pytest.fixture
def zoneTriangleA():
    coordinates = [
          [
            [
              -121.93416595458983,
              37.305464062126
            ],
            [
              -121.96420669555664,
              37.27036454209622
            ],
            [
              -121.91150665283203,
              37.27186719156333
            ],
            [
              -121.93416595458983,
              37.305464062126
            ]
          ]
    ]
    zone = Zone(coordinates_list=coordinates)
    return zone

@pytest.fixture
def zoneRectangleB():
    coordinates = [
          [
            [
              -122.04145431518556,
              37.344368504994286
            ],
            [
              -122.0328712463379,
              37.344368504994286
            ],
            [
              -122.0328712463379,
              37.35760507144896
            ],
            [
              -122.04145431518556,
              37.35760507144896
            ],
            [
              -122.04145431518556,
              37.344368504994286
            ]
          ]
        ]
    zone = Zone(coordinates_list=coordinates)
    return zone

@pytest.fixture
def coordinatesZoneB():
    coordinates = [
          [
            [
              -122.04145431518556,
              37.344368504994286
            ],
            [
              -122.0328712463379,
              37.344368504994286
            ],
            [
              -122.0328712463379,
              37.35760507144896
            ],
            [
              -122.04145431518556,
              37.35760507144896
            ],
            [
              -122.04145431518556,
              37.344368504994286
            ]
          ]
        ]
    return coordinates

# Regular test case testing within, outside, on line
@pytest.fixture
def apiResponseTestCaseA():
    json0Within = '''{
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                -121.93296432495117,
                37.29139890536388
                ]
            }
            },
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                [
                    [
                    -121.93416595458983,
                    37.305464062126
                    ],
                    [
                    -121.96420669555664,
                    37.27036454209622
                    ],
                    [
                    -121.91150665283203,
                    37.27186719156333
                    ],
                    [
                    -121.93416595458983,
                    37.305464062126
                    ]
                ]
                ]
            }
            }
        ]
        }
    '''
    json1Outside = '''{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-121.9432252407074,37.32532129713498]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-121.93468093872069,37.33631625612842],[-121.96249008178712,37.33617976989369],[-121.96523666381836,37.304644804751106],[-121.93708419799805,37.30491789153446],[-121.93777084350586,37.31761533167621],[-121.95150375366211,37.316796206705085],[-121.95219039916992,37.32607910032697],[-121.93708419799805,37.32648861334206],[-121.93468093872069,37.33631625612842]]]}}]}'''
    json2OnLine = '''{
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                -122.0328712463379,
                37.351803043153
                ]
            }
            },
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                [
                    [
                    -122.04145431518556,
                    37.344368504994286
                    ],
                    [
                    -122.0328712463379,
                    37.344368504994286
                    ],
                    [
                    -122.0328712463379,
                    37.35760507144896
                    ],
                    [
                    -122.04145431518556,
                    37.35760507144896
                    ],
                    [
                    -122.04145431518556,
                    37.344368504994286
                    ]
                ]
                ]
            }
            }
        ]
        }'''
    return [json0Within, json1Outside, json2OnLine]

# Regular test case testing within, within, on line
@pytest.fixture
def apiResponseTestCaseB():
    json0Within = '''{
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                -121.93296432495117,
                37.29139890536388
                ]
            }
            },
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                [
                    [
                    -121.93416595458983,
                    37.305464062126
                    ],
                    [
                    -121.96420669555664,
                    37.27036454209622
                    ],
                    [
                    -121.91150665283203,
                    37.27186719156333
                    ],
                    [
                    -121.93416595458983,
                    37.305464062126
                    ]
                ]
                ]
            }
            }
        ]
        }
    '''
    json1Within = '''{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
          -121.9432252407074,
          37.33534129713498
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -121.93468093872069,
              37.33631625612842
            ],
            [
              -121.96249008178712,
              37.33617976989369
            ],
            [
              -121.96523666381836,
              37.304644804751106
            ],
            [
              -121.93708419799805,
              37.30491789153446
            ],
            [
              -121.93777084350586,
              37.31761533167621
            ],
            [
              -121.95150375366211,
              37.316796206705085
            ],
            [
              -121.95219039916992,
              37.32607910032697
            ],
            [
              -121.93708419799805,
              37.32648861334206
            ],
            [
              -121.93468093872069,
              37.33631625612842
            ]
          ]
        ]
      }
    }
  ]
}'''
    json2OnLine = '''{
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                -122.0328712463379,
                37.351803043153
                ]
            }
            },
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                [
                    [
                    -122.04145431518556,
                    37.344368504994286
                    ],
                    [
                    -122.0328712463379,
                    37.344368504994286
                    ],
                    [
                    -122.0328712463379,
                    37.35760507144896
                    ],
                    [
                    -122.04145431518556,
                    37.35760507144896
                    ],
                    [
                    -122.04145431518556,
                    37.344368504994286
                    ]
                ]
                ]
            }
            }
        ]
        }'''
    return [json0Within, json1Within, json2OnLine]

@pytest.fixture
def ids():
    return [1,2,3]

@pytest.fixture
def statusURL():
    return "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/"

@pytest.fixture
def clinicianInterface(ids):
    return ClinicianInterface(clinician_ids=ids)

@pytest.fixture
def clinicianStatusAPIInterface():
    return ClinicianStatusAPIInterface()

@pytest.fixture
def emailInterface():
    return EmailInterface()

# def test_newTest():
#     with requests_mock.Mocker() as m:
#         m.get("http://test.com", text='data')
#         assert 'data' != requests.get("http://test.com").text

def test_clinicianWithinZoneA(clinicianWithinA, zoneTriangleA):
    within = zoneTriangleA.contains(clinicianWithinA)
    assert within

def test_clinicianOutsideZoneA(clinicianOutsideA, zoneTriangleA):
    within = zoneTriangleA.contains(clinicianOutsideA)
    assert not within

def test_clinicianWithinZoneB(clinicianWithinB, zoneRectangleB):
    within = zoneRectangleB.contains(clinicianWithinB)
    assert within

def test_clinicianOutsideZoneA(clinicianOnLineB, zoneRectangleB):
    within = zoneRectangleB.contains(clinicianOnLineB)
    assert within

def test_APINormal(statusURL, ids, clinicianInterface, clinicianStatusAPIInterface, apiResponseTestCaseA):
    def verify_safety_core_logic(index, id, apiMockResponse):
        m.get(statusURL + str(id), json=json.loads(apiMockResponse[index]))
        clinician_coordinates, zone_coordinates = clinicianStatusAPIInterface.get_clinician_status(clinician_id=id)
                    
        clinicianInterface.update_clinician_location(clinician_id=id, clinician_coordinates=clinician_coordinates)
        clinicianInterface.update_zone(clinician_id=id, zone_coordinates=zone_coordinates)
                    
        within, new_broadcast = clinicianInterface.check_clinician_within_zone(clinician_id=id)
        return within, new_broadcast
    assertions = [(True, False), (False, True), (True, False)]
    with requests_mock.Mocker() as m:
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseA)
            assert assertions[index][0] == within
            assert assertions[index][1] == new_broadcast

def test_APIDoubleBroadcast(statusURL, ids, clinicianInterface, clinicianStatusAPIInterface, apiResponseTestCaseA):
    def verify_safety_core_logic(index, id, apiMockResponse):
        m.get(statusURL + str(id), json=json.loads(apiMockResponse[index]))
        clinician_coordinates, zone_coordinates = clinicianStatusAPIInterface.get_clinician_status(clinician_id=id)
                    
        clinicianInterface.update_clinician_location(clinician_id=id, clinician_coordinates=clinician_coordinates)
        clinicianInterface.update_zone(clinician_id=id, zone_coordinates=zone_coordinates)
                    
        within, new_broadcast = clinicianInterface.check_clinician_within_zone(clinician_id=id)
        return within, new_broadcast

    with requests_mock.Mocker() as m:
        assertionsFirst = [(True, False), (False, True), (True, False)]
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseA)
            assert assertionsFirst[index][0] == within
            assert assertionsFirst[index][1] == new_broadcast

        assertionsSecond = [(True, False), (False, False), (True, False)]
        # Test double broadcast
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseA)
            
            assert assertionsSecond[index][0] == within
            assert assertionsSecond[index][1] == new_broadcast

def test_APIBroadcastReset(statusURL, ids, clinicianInterface, clinicianStatusAPIInterface, apiResponseTestCaseA, apiResponseTestCaseB):
    def verify_safety_core_logic(index, id, apiMockResponse):
        m.get(statusURL + str(id), json=json.loads(apiMockResponse[index]))
        clinician_coordinates, zone_coordinates = clinicianStatusAPIInterface.get_clinician_status(clinician_id=id)
                    
        clinicianInterface.update_clinician_location(clinician_id=id, clinician_coordinates=clinician_coordinates)
        clinicianInterface.update_zone(clinician_id=id, zone_coordinates=zone_coordinates)
                    
        within, new_broadcast = clinicianInterface.check_clinician_within_zone(clinician_id=id)
        return within, new_broadcast

    with requests_mock.Mocker() as m:
        assertionsFirst = [(True, False), (False, True), (True, False)]
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseA)
            assert assertionsFirst[index][0] == within
            assert assertionsFirst[index][1] == new_broadcast

        assertionsSecond = [(True, False), (True, False), (True, False)]
        # Test double broadcast
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseB)
            
            assert assertionsSecond[index][0] == within
            assert assertionsSecond[index][1] == new_broadcast

        assertionsThird = [(True, False), (False, True), (True, False)]
        for index, id in enumerate(ids):
            within, new_broadcast = verify_safety_core_logic(index, id, apiResponseTestCaseA)
            assert assertionsThird[index][0] == within
            assert assertionsThird[index][1] == new_broadcast
        
# with pytest.raises(ValueError, match='must be 0 or None'):