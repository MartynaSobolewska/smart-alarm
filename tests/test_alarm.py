import pytest
import sys
sys.path.append(".")
import sched
import time

def print_a(a:str):
    print(a)

s = sched.scheduler(time.time, time.sleep)
s.enter(8,1,print_a, "a")
s.run()