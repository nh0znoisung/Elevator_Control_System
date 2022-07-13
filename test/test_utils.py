import unittest, sys, pytest
from unittest.mock import MagicMock
from src.utils import *
# from utils import * # will test a little
# sys.path.append('../')

class TestSetting:
    def test_init(self):
        setting = Setting()
        assert setting.DELAY_TIME == 1.5
        assert setting.FLOOR_NUMS == 10
        assert setting.ELEVATOR_NUMS == 3
        for i in range(setting.FLOOR_NUMS):
            assert setting.LIST_FLOOR[i].floor_number == i

        for i in range(setting.ELEVATOR_NUMS):
            assert setting.LIST_ELEVATOR[i].elevator_number == i
    
    def test_init_params(self): 
        setting = Setting(10, 20, 15)
        assert setting.DELAY_TIME == 10
        assert setting.FLOOR_NUMS == 20
        assert setting.ELEVATOR_NUMS == 15
        for i in range(setting.FLOOR_NUMS):
            assert setting.LIST_FLOOR[i].floor_number == i

        for i in range(setting.ELEVATOR_NUMS):
            assert setting.LIST_ELEVATOR[i].elevator_number == i
    
    def test_set_floor(self):
        setting = Setting()
        setting.set_floor(20)
        assert setting.FLOOR_NUMS == 20
        for i in range(setting.FLOOR_NUMS):
            assert setting.LIST_FLOOR[i].floor_number == i

    def test_set_elevator(self):
        setting = Setting()
        setting.set_elevator(15)
        assert setting.ELEVATOR_NUMS == 15
        for i in range(setting.ELEVATOR_NUMS):
            assert setting.LIST_ELEVATOR[i].elevator_number == i

class TestSystem:
    def test_init(self):
        system = System()
        assert system.is_running == False

    def test_setup(self, monkeypatch):
        system = System()
        monkeypatch.setattr(threading.Thread, "start", lambda _: None)

        system.setup()
        assert system.is_running == True
    
    def test_terminate(self, monkeypatch):
        system = System()
        monkeypatch.setattr(threading.Thread, "start", lambda _: None)
        monkeypatch.setattr(threading.Thread, "join", lambda _: None)

        system.setup()
        system.terminate()
        assert system.is_running == False

class TestElevator:
    def test_init(self):
        elevator = Elevator(1)
        assert elevator.elevator_number == 1
        assert elevator.target_floor == 0
        assert elevator.curr_floor == 0
        assert elevator.requests == deque([])

class TestFloor:
    def test_init(self):
        floor = Floor(10)
        assert floor.floor_number == 10
        assert floor.requests == []
    
    def test_add_request(self, monkeypatch):
        floor = Floor(10)
        request = Request()
        monkeypatch.setattr(Floor, "ping", lambda x,y: None)
        floor.add_request(request, 1)
        assert len(floor.requests) == 1
        assert floor.requests[0] == request

    def test_release_request(self, monkeypatch):
        floor = Floor(10)
        monkeypatch.setattr(Floor, "ping", lambda x,y: None)
        request1 = Request()
        floor.add_request(request1, 1)

        request2 = Request()
        floor.add_request(request2, 2)

        floor.release_request()
        assert len(floor.requests) == 0
        assert request1.is_done == True
        assert request2.is_done == True
