from safety_interface import SafetyInterface
from typing import List
import time
import schedule

class Main:
    def __init__(self, clinician_ids: List[int]):
        if not isinstance(clinician_ids, list):
            raise TypeError("Argument clinician_ids of invalid type. Expected a list of integers.")
        elif len(clinician_ids) != 0 and (not isinstance(clinician_ids[0],int)):
            raise TypeError("Argument clinician_ids of invalid type. Expected a list of integers.")

        self.safetyInterface = SafetyInterface(clinician_ids=clinician_ids)

    def run(self):
        schedule.every(1).minutes.do(
            self.safetyInterface.verify_safety
        )
        while True:
            schedule.run_pending()
            time.sleep(30.0)


if __name__ == '__main__':
    main = Main([1,2,3,4,5,6])
    main.run()