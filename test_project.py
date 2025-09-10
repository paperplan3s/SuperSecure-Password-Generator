from project import check_special, check_upper, check_len
import pytest


def test_check_special():
    assert check_special("Hello") == False
    assert check_special("Hello!") == True
    assert check_special("H*llo") == True

def test_check_upper():
    assert check_upper("hello") == False
    assert check_upper("Hello") == True
    assert check_upper("hellO") == True


def test_check_len():
    assert check_len("pass") == False
    assert check_len("password") == True
    assert check_len("hunter2") == True

