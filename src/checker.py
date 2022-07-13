# from utils import *
import os

class Checker:
    # floor_number. Fastapi make sure it is Int
    # From >= 0 and < upper_bound
    # upper_bound > 0
    def check_floor(self, floor_number: int, upper_bound: int):
        if floor_number < 0:
            raise Exception("The floor number can not be negative")
        elif floor_number >= upper_bound:
            raise Exception("The floor number is out of range")
        return True

    def check_elevator(self, elevator_number: int, upper_bound: int):
        if elevator_number < 0:
            raise Exception("The elevator number can not be negative")
        elif elevator_number >= upper_bound:    
            raise Exception("The elevator number is out of range")
        return True

    def check_positive(self, number: int):
        if number <= 0:
            raise Exception("The input must be positive")
        return True