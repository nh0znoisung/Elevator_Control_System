import time
from collections import deque
import threading
from src.checker import Checker


class Request:
    is_done: bool
    def __init__(self):
        self.is_done = False

    def __del__(self):
        self.is_done = False


class Floor:
    requests: list
    floor_number: int
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.requests = []
    
    def __del__(self):
        self.floor_number = -1 # Excetion number
        self.requests = []
    
    def ping(self, elevator_number: int): # Ping to Elevator
        # Only 1 elevator is global
        # print("Ping to elevator " + str(elevator_number))
        setting.LIST_ELEVATOR[elevator_number].requests.append(self.floor_number)
        # print(setting.LIST_ELEVATOR[elevator_number].requests)

    def add_request(self, request: Request, elevator_number: int):
        # print("Add request ele " + str(elevator_number))
        if len(self.requests) == 0:
            # print("Hello Ping")
            self.ping(elevator_number)
        self.requests.append(request)
    
    def release_request(self):
        for request in self.requests:
            request.is_done = True
        self.requests = [] # Need mutex lock


class Elevator:
    elevator_number: int
    requests: deque
    curr_floor: int
    target_floor: int

    def __init__(self, elevator_number):
        self.requests = deque()
        self.curr_floor = 0
        self.target_floor = 0
        self.elevator_number = elevator_number

    def move(self):
        # Move from curr_floor to target_floor
        print("Elevator {:6s} The elevator is moving from floor {} to floor {}".format(str(self.elevator_number)+':', self.curr_floor, self.target_floor))
        up = True if self.target_floor > self.curr_floor else False
        while True:
            print("Elevator {:6s} The elevator is on floor {}".format(str(self.elevator_number)+':', self.curr_floor))
            if self.curr_floor == self.target_floor:
                break
            tic = time.time()
            while True:
                toc = time.time()
                if toc - tic > setting.DELAY_TIME:
                    break
            # Go up or down
            if up:
                self.curr_floor += 1
            else:
                self.curr_floor -= 1
        print("Elevator {:6s} The elevator finished journey at floor {}".format(str(self.elevator_number)+':', self.target_floor))


    def run(self, lock):
        while True:   
            if not system.is_running:
                continue
            if len(self.requests) == 0:
                continue
            
            # Get request
            self.target_floor = self.requests[0]

            # Move
            self.move()

            # Come and release the request in floor
            lock.acquire()
            setting.LIST_FLOOR[self.requests[0]].release_request()
            lock.release()
            self.requests.popleft()


class Setting:
    DELAY_TIME: int
    FLOOR_NUMS: int
    LIST_FLOOR: list
    ELEVATOR_NUMS: int  
    LIST_ELEVATOR: list

    # Default settings
    def __init__(self, delay_time = 1.5, floor_number = 10, elevator_number = 3):
        self.DELAY_TIME = delay_time
        self.FLOOR_NUMS = floor_number
        self.LIST_FLOOR = [Floor(i) for i in range(self.FLOOR_NUMS)]
        self.ELEVATOR_NUMS = elevator_number
        self.LIST_ELEVATOR = [Elevator(i) for i in range(self.ELEVATOR_NUMS)]

    def set_floor(self, floor_number: int):
        self.FLOOR_NUMS = floor_number
        self.LIST_FLOOR = [Floor(i) for i in range(self.FLOOR_NUMS)]

    def set_elevator(self, elevator_number: int):
        self.ELEVATOR_NUMS = elevator_number
        self.LIST_ELEVATOR = [Elevator(i) for i in range(self.ELEVATOR_NUMS)]
        lock = threading.Lock()
        system.LIST_THREAD = [threading.Thread(target=system.run_elevator, args=(i,lock,)) for i in range(self.ELEVATOR_NUMS)]

class System:
    is_running: bool
    LIST_THREAD: list

    def run_elevator(self, elevator_number, lock):
        setting.LIST_ELEVATOR[elevator_number].run(lock)

    def __init__(self):
        self.is_running = False
        lock = threading.Lock()
        self.LIST_THREAD = [threading.Thread(target=self.run_elevator, args=(i,lock,)) for i in range(setting.ELEVATOR_NUMS)]

    def setup(self):
        # Using thread
        self.is_running = True
        # if not self.is_first_set:
        #     self.is_first_set = True
        for i in range(setting.ELEVATOR_NUMS):
            self.LIST_THREAD[i].start()

    def terminate(self):
        # Join thread
        self.is_running = False
        for i in range(setting.ELEVATOR_NUMS):
            self.LIST_THREAD[i].join()

checker = Checker()
setting = Setting()
system = System()