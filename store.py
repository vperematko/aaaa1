"""CSC148 Assignment 1 - Modelling a Grocery Store (Task 1a)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in a grocery store.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from __future__ import annotations
from typing import List, Optional, TextIO
import json
# Use this constant in your code
EXPRESS_LIMIT = 7


# DOCSTRINGS DONE
class GroceryStore:
    """A grocery store.

    === Attributes ===
    _regular_count: How many regular lines are open.
    _express_count: How many express lines are open.
    _self_serve_count: How many self-serve lines are open.
    _line_capacity: maximum amount of people allowed in each line
    _line_list: list of all the lines open, following representation invariants

    === Representation Invariant ===
    - _line_list is ordered in the following order:
    RegularLine, ExpressLine, SelfServeLine
    - _line_capacity is the same for all lines
    """
    _regular_count: int
    _express_count: int
    _self_serve_count: int
    _line_capacity: int
    _line_list: List[Any]

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.
        >>> import io
        >>> config_file = io.StringIO('{"regular_count":3,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.get_info('_regular_count') == 3
        True
        >>> g.get_info('_express_count') == 0
        True
        >>> g.get_info('_self_serve_count') == 1
        True
        >>> g.get_info('_line_capacity') == 10
        True
        """
        working = json.load(config_file)
        self._regular_count = working.get('regular_count')
        self._express_count = working.get('express_count')
        self._self_serve_count = working.get('self_serve_count')
        self._line_capacity = working.get('line_capacity')
        self._zz = 0
        self._line_list = []

        for _ in range(self._regular_count):
            self._line_list.append(RegularLine(self._line_capacity))
        for _ in range(self._express_count):
            self._line_list.append(ExpressLine(self._line_capacity))
        for _ in range(self._self_serve_count):
            self._line_list.append(SelfServeLine(self._line_capacity))

    def get_info(self, name: str) -> int:
        """Return requested info from input file. Allows indirect access to
        private attributes.
        Primarily to be used in doctests and pytests
        >>> import io
        >>> config_file = io.StringIO('{"regular_count":3,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.get_info('_regular_count')
        3
        >>> g.get_info('_express_count')
        0
        >>> g.get_info('_self_serve_count')
        1
        >>> g.get_info('_line_capacity')
        10
        """
        if name == '_regular_count':
            return self._regular_count
        elif name == '_express_count':
            return self._express_count
        elif name == '_self_serve_count':
            return self._self_serve_count
        elif name == '_line_capacity':
            return self._line_capacity
        else:
            return 0

    def get_line_list(self) -> List:
        """Return the list of lines in this GroceryStore.
        >>> import io
        >>> config_file = io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> result = g.get_line_list()
        >>> len(result) == 1
        True
        """
        return self._line_list

    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join.

        Return the index of the line that the customer joined.
        Must use the algorithm from the handout.

        When a new customer arrives, they join the open line with the fewest
        number of customers that they are allowed to join, choosing the one
        with the lowest index (as represented by the grocery store)
        if there is a tie.

        When there are no lines the customer can join, the “new customer” event
        should go back into the container, and have its timestamp increased by
        1 (representing trying to join a line again at the next time interval.)

        Return -1 if there is no line available for the customer to join.
        >>> import io
        >>> enter_line_config_file = io.StringIO('{"regular_count":1,"express_count":0,"self_serve_count":1,"line_capacity":1}')
        >>> g1 = GroceryStore(enter_line_config_file)
        >>> g1._zz = 1
        >>> customer = Customer('Bill', [Item('banana', 5)])
        >>> g1.enter_line(customer)
        0
        >>> customer = Customer('nye', [Item('apple', 6)])
        >>> g1.enter_line(customer)
        1
        >>> customer= Customer('the science guy', [Item('apple', 6)])
        >>> g1.enter_line(customer)
        -1
        """
        if self._zz == 1:
            self._zz += 1
        lowest_index = None
        lowest_queue = 200000000
        for i, line in enumerate(self.get_line_list()):
            if line.can_accept(customer):
                queue_length = len(line.queue)
                if queue_length < lowest_queue:
                    lowest_queue = queue_length
                    lowest_index = i
        if lowest_index is None:
                return -1
        self._line_list[lowest_index].queue.append(customer)
        return lowest_index

    def line_is_ready(self, line_number: int) -> bool:
        """Return True iff checkout line <line_number> is ready to start a
        checkout. Thus, line_is_ready should return True
        if and only if there is exactly one customer in line
        >>> import io
        >>> config_file = \
        io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.enter_line(Customer('the science guy', [Item('apple', 6)]))
        0
        >>> g.enter_line(Customer('bill nye', [Item('banana', 5)]))
        0
        >>> g.line_is_ready(0)
        False
        """
        line = self._line_list[line_number]
        return len(line.queue) == 1

    def start_checkout(self, line_number: int) -> int:
        """Return the time it will take to check out the next customer in
        line <line_number>

        >>> import io
        >>> config_file = \
        io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.enter_line(Customer('the science guy', [Item('apple', 6)]))
        0
        >>> g.start_checkout(0)
        12
        """
        return self.get_line_list()[line_number].start_checkout()

    def complete_checkout(self, line_number: int) -> bool:
        """Return True iff there are customers remaining to be checked out in
        line <line_number>
        >>> import io
        >>> config_file = \
        io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.enter_line(Customer('the science guy', [Item('apple', 6)]))
        0
        >>> g.complete_checkout(0)
        True
        """
        line = self._line_list[line_number]
        return len(line.queue) >= 1

    def close_line(self, line_number: int) -> List[Customer]:
        """Close checkout line <line_number> and return the customers from
        that line who are still waiting to be checked out.
        >>> import io
        >>> config_file = \
        io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.enter_line(Customer('the', [Item('apple', 6)]))
        0
        >>> g.enter_line(Customer('science', [Item('banana', 7)]))
        0
        >>> g.enter_line(Customer('guy', [Item('carrot', 8)]))
        0
        >>> len(g.close_line(0)) == 2
        True
        """
        line = self._line_list[line_number]
        return line.close()

    def get_first_in_line(self, line_number: int) -> Optional[Customer]:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.
        >>> import io
        >>> config_file = \
         io.StringIO('{"regular_count":0,"express_count":0,"self_serve_count":1,"line_capacity":10}')
        >>> g = GroceryStore(config_file)
        >>> g.enter_line(Customer('the science guy', [Item('apple', 6)]))
        0
        >>> g.get_first_in_line(0).name == 'the science guy'
        True
        """
        line = self._line_list[line_number]
        if len(line.queue) == 0:
            return None
        else:
            return line.queue[0]


# DOCSTRINGS DONE
class Customer:
    """A grocery store customer.

    === Attributes ===
    name: A unique identifier for this customer.
    arrival_time: The time this customer joined a line.
    _items: The items this customer has.

    === Representation Invariant ===
    arrival_time >= 0 if this customer has joined a line, and -1 otherwise
    """
    name: str
    arrival_time: int
    _items: List[Item]

    def __init__(self, name: str, items: List[Item]) -> None:
        """Initialize a customer with the given <name>, an initial arrival time
         of -1, and a copy of the list <items>.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda.arrival_time
        -1
        """
        self.name = name
        self.arrival_time = -1
        self._items = items

    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def get_item_time(self) -> int:
        """Return the number of seconds it takes to check out this customer.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.get_item_time()
        10
        """
        total = 0
        for item in self._items:
            total += item.get_time()
        return total

    def get_items(self) -> List[Item]:
        """Return a list of items for this customer

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.get_items()[0].get_item_name()
        'bananas'
        >>> c.get_items()[0].get_time()
        7
        >>> c.get_items()[1].get_item_name()
        'cheese'
        >>> c.get_items()[1].get_time()
        3
        """
        return self._items


# DOCSTRINGS DONE
class Item:
    """A class to represent an item to be checked out.

    Do not change this class.

    === Attributes ===
    name: the name of this item
    _time: the amount of time it takes to checkout this item
    """
    name: str
    _time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new time with <name> and <time>.

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item.get_time()
        7
        """
        self.name = name
        self._time = time

    def get_time(self) -> int:
        """Return how many seconds it takes to checkout this item.

        >>> item = Item('bananas', 7)
        >>> item.get_time()
        7
        """
        return self._time

    def get_item_name(self) -> str:
        """Return the name of this item
        >>> item = Item('bananas', 7)
        >>> item.get_item_name()
        'bananas'
        """
        return self.name


class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class; subclasses are responsible for implementing
    start_checkout().

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order.

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine.

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        self.capacity = capacity
        self.is_open = True
        self.queue = []

    def __len__(self) -> int:
        """Return the size of this CheckoutLine.
        >>> line = CheckoutLine(10)
        >>> line.accept(Customer('bill', []))
        True
        >>> line.__len__()
        1
        """
        return len(self.queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
        >>> line = CheckoutLine(10)
        >>> customer = Customer('the science guy', [Item('banana', 5)])
        >>> line.can_accept(customer)
        True
        """
        return self.is_open and (len(self.queue) < self.capacity)

    def accept(self, customer: Customer) -> bool:
        """Accept <customer> at the end of this CheckoutLine.
        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> line.queue == [c1]
        True
        """
        if self.can_accept(customer):
            self.queue.append(customer)
            return True
        return False

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.
        Return the time it will take to checkout the next customer.
        Assume that there is a customer in line when this is called.
        """
        raise NotImplementedError

    def complete_checkout(self) -> bool:
        """Finish the checkout for this CheckoutLine.

        Return whether there are any remaining customers in the line.
        Customer is in the queue until they are done checking out.
        >>> line = CheckoutLine(10)
        >>> line.accept(Customer('bill', []))
        True
        >>> line.accept(Customer('nye', []))
        True
        >>> line.complete_checkout()
        True
        """
        self.queue.pop(0)
        return len(self.queue) >= 1

    def close(self) -> List[Customer]:
        """Close this line.

        Return a list of all customers that need to be moved to another line.
        The last person in line will join another queue (first) as the line
        closes, and the rest of the people will join each second after.

        >>> line = CheckoutLine(10)
        >>> line.accept(Customer('bill', [Item('cheese', 3)]))
        True
        >>> line.accept(Customer('nye', [Item('eggs', 4)]))
        True
        >>> line.close()[0].name == 'nye'
        True
        """
        i = 0
        result = []
        reverse_queue = self.queue[::-1]
        while i != (len(self.queue) - 1):
            to_move = reverse_queue.pop(i)
            result.append(to_move)
            i += 1
        return result

        # logically trace through
        # consider using for

class RegularLine(CheckoutLine):
    """A regular CheckoutLine.

    Any customer can join the line, if there is room.
    The time required to checkout is equal to the total time required
    for items the customer has.

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order.

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.
    """

    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty RegularLine .

        >>> line = RegularLine(1) #Rewrite this doctest
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        super().__init__(capacity)

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.

        Return the time it will take to checkout the next customer.
        Assume that there is a customer in line when this is called.

        >>> line = RegularLine(10)
        >>> line.accept(Customer('bill', [Item('cheese', 3)]))
        True
        >>> line.start_checkout()
        3
        """
        total_time = 0
        customer = self.queue[0]
        items = customer.get_items()
        if customer is not None:
            for item in items:
                time = item.get_time()
                total_time += time
        return total_time


class ExpressLine(CheckoutLine):
    """An express CheckoutLine.

    Customers can only enter the line if they have fewer than 8 items,
    and there is room. The time required to checkout is equal to the
    total time required for items the customer has.

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order.

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.

    capacity: int
    is_open: bool
    queue: List[Customer]
    """
    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty ExpressLine .

        >>> line = ExpressLine(1) #Rewrite this doctest
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        super().__init__(capacity)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
        Assume that there is a customer in line when this is called.

        This method overrides CheckoutLine.can_accept due to the additional max
        item parameter required.
        >>> line = ExpressLine(10)
        >>> customer = Customer('the science guy', [Item('banana', 5)])
        >>> line.can_accept(customer)
        True
        """
        return self.is_open and \
                (len(self.queue) < self.capacity) and \
                (customer.num_items() < EXPRESS_LIMIT)

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.

        Return the time it will take to checkout the next customer.
        Assume that there is a customer in line when this is called.
        >>> line = ExpressLine(10)
        >>> line.accept(Customer('bill', [Item('cheese', 3)]))
        True
        >>> line.accept(Customer('nye', [Item('eggs', 4)]))
        True
        >>> line.start_checkout()
        3
        """
        total_time = 0
        customer = self.queue[0]
        items = customer.get_items()
        if customer is not None:
            for item in items:
                time = item.get_time()
                total_time += time
        return total_time


class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.

    Any customer can join the line, if there is room.
    The time required to checkout is equal to twice the total time
    required for items the customer has.

    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty Self Serve Line.

        >>> line = SelfServeLine(1) #Rewrite this doctest
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        super().__init__(capacity)

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.

        Return the time it will take to checkout the next customer.
        >>> line = SelfServeLine(10)
        >>> line.accept(Customer('bill', [Item('cheese', 3)]))
        True
        >>> line.accept(Customer('nye', [Item('eggs', 4)]))
        True
        >>> line.start_checkout()
        6
        """
        total_time = 0
        customer = self.queue[0]
        items = customer.get_items()
        if customer is not None:
            for item in items:
                time = item.get_time()
                total_time += time
        return total_time * 2


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest'],
        'disable': ['W0613']})


    # import io
    # config_file = io.StringIO('{"regular_count":1,"express_count":0,"self_serve_count":1,"line_capacity":1}')
    # g = GroceryStore(config_file)
    # customer_one = Customer('bill', [Item('banana', 5)])
