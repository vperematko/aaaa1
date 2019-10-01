"""CSC148 Assignment 1: Sample tests

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.

Warning: This is an extremely incomplete set of tests!

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from simulation import GroceryStoreSimulation

CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
'''


def test_simulation() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE))
    stats = gss.run(StringIO(EVENT_FILE))
    assert stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


if __name__ == '__main__':
    import pytest
    pytest.main(['a1_sample_test.py'])
