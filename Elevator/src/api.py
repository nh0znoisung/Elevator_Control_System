from fastapi import FastAPI, BackgroundTasks
import numpy as np
from src.utils import *
from src.checker import *

app = FastAPI()


def check_release(request):
    while not request.is_done:
        pass
    return True

def setup():
    system.setup()

def end():
    system.terminate()

@app.post("/start-system/{floor_number}/{elevator_number}")
async def start_system(floor_number: int, elevator_number: int, background_tasks: BackgroundTasks):
    if system.is_running:
        return "The elevator is already running. You can re-config the settings after restarting the system."
    
    # Validation input
    try:
        checker.check_positive(floor_number)
        checker.check_positive(elevator_number)
    except Exception as e:
        return e

    setting.set_floor(floor_number)
    setting.set_elevator(elevator_number)

    background_tasks.add_task(setup)
    print("The elevator launched successfully with {} floors and {} elevators.".format(floor_number, elevator_number))
    return "The elevator launched successfully with {} floors and {} elevators.".format(floor_number, elevator_number)

@app.post("/end-system")
async def end_system(background_tasks: BackgroundTasks):
    background_tasks.add_task(end)
    return "The elevator is stopped."

@app.post("/inside/{floor_number}/{elevator_number}")
def send_inside(floor_number: int, elevator_number: int):
    if not system.is_running:
        return "The elevator is not running. Please launch the elevator first."
    
    # Validation input
    try:
        checker.check_floor(floor_number, setting.FLOOR_NUMS)
        checker.check_elevator(elevator_number, setting.ELEVATOR_NUMS)
    except Exception as e:
        return e

    request = Request()

    setting.LIST_FLOOR[floor_number].add_request(request, elevator_number)
    check_release(request)
    return "The request is completed."


# Outside: Ping to specific elevator
@app.post("/outside/{floor_number}")
def send_outside(floor_number: int):
    if not system.is_running:
        return "The elevator is not running. Please launch the elevator first."
    
    # Validation input    
    try:
        checker.check_floor(floor_number, setting.FLOOR_NUMS)
    except Exception as e:
        return e

    request = Request()

    # Which elevator have min request
    elevator_request = np.array([len(elevator.requests) for elevator in setting.LIST_ELEVATOR])
    elevator_number_min = np.argmax(np.random.random(elevator_request.shape) * (elevator_request == elevator_request.min()))

    setting.LIST_FLOOR[floor_number].add_request(request, elevator_number_min)
    check_release(request)
    return "The request is completed. The elevator {} came.".format(elevator_number_min)