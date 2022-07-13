# https://betterprogramming.pub/how-to-create-a-post-request-in-fastapi-3dbd017dd998/
import unittest, sys, pytest
from unittest.mock import MagicMock
from src.checker import *
# from utils import * # will test a little
# sys.path.append('../')


class TestCheckFloor:
    def test_negative_basic(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(-1,1)

    def test_negative_complex_small(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(-1,11111111)
    
    def test_negative_complex_big_1(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(-12234567, 1234567)
    
    def test_negative_complex_big_2(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(-100, 100)

    def test_positive_basic_1(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(100, 100)
    
    def test_positive_basic_2(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(101, 100)

    def test_positive_complex(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_floor(10000001, 10000000)

    def test_true_small(self):
        checker = Checker()
        assert checker.check_floor(0,1) == True

    def test_true_big(self):
        checker = Checker()
        assert checker.check_floor(9999999,10000000) == True

class TestCheckElevator:
    def test_negative_basic(self):
        checker = Checker()
        with pytest.raises(Exception) as e:
            checker.check_elevator(-11,718)

    def test_negative_complex_small(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_elevator(-2,6789541)
    
    def test_negative_complex_big_1(self):
        checker = Checker()
        with pytest.raises(Exception) as e:
            checker.check_elevator(-123428567, 9991234567)
    
    def test_negative_complex_big_2(self):
        checker = Checker()
        with pytest.raises(Exception) as e:
            checker.check_elevator(-12234512267, 87)

    def test_positive_basic_1(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_elevator(100, 100)
    
    def test_positive_basic_2(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_elevator(101, 100)

    def test_positive_complex(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_elevator(10000001, 10000000)

    def test_true_small(self):
        checker = Checker()
        assert checker.check_elevator(0,1) == True

    def test_true_big(self):
        checker = Checker()
        assert checker.check_elevator(9999999,10000000) == True

class TestCheckPositive:
    def test_negative_basic(self):
        checker = Checker()
        with pytest.raises(Exception) as e:
            checker.check_positive(-1)
    
    def test_negative_complex(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_positive(-776897681)
        
    def test_zero(self):
        checker = Checker()
        with pytest.raises(Exception):
            checker.check_positive(0)

    def test_positive_basic(self):
        checker = Checker()
        assert checker.check_positive(1) == True
    
    def test_positive_complex(self):
        checker = Checker()
        assert checker.check_positive(1876567823) == True