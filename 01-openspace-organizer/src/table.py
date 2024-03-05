class Seat:
    '''This is were people sit!'''

    def __init__(self, free: bool = True, occupant: str = None) -> bool: #This class creates a seat wich is occupied or not
        self.free = free
        self.occupant = occupant

#`set_occupant(name)` which allows the program to assign someone a seat if it's free
    def set_occupant(self, name: str):
        self.name = name
        if self.free:
            self.free = False
            self.occupant = name
    
# `remove_occupant()` which removes someone from a seat and returns the name of the person occupying the seat before
    def remove_occupant(self, occupant: str) -> str:
        if not self.free:
            last_occupant = self.occupant # Used to temporarily store the current occupant of the seat in the occupant variable...
            self.occupant = "" # ...before removing him/her
            self.free = True # mark the seat as vacant after the occupant has been removed
        print(last_occupant)
        return last_occupant
        
class Table:
    '''This is were people gather around!'''

    def __init__(self, capacity: int = 4) -> list: # This class creates a table wich multiples seats
        self.capacity = capacity
        self.seats = [Seat() for _ in range(capacity)] #  Initializes a list of seat objects with the required capacity

# Go on and add some methods to the class:
# `has_free_spot()` that returns a boolean (`True` if a spot is available)
    def has_free_spot(self) -> bool:
        free_spot = False
        for seat in self.seats: # iterates through the seats list of the Table object...
            if seat.free: # and checks if any seat is free
                free_spot = True
                break
        return free_spot
    
# `assign_seat(occupant)` that places someone at the table
    def assign_seat(self, name: str) -> bool:
        self.name = name
        if self.has_free_spot():
            for seat in self.seats:
                if seat.free:
                    seat.set_occupant(name)
                    return True
        else:
            return False

#`capacity_left()` that returns an integer of empty seats left at the table
    def capacity_left(self) -> int:
        count = 0 # initializes a counter count to 0
        for seat in self.seats: #  it iterates through the seats list...
            if seat.free:
                count += 1 # and increments the counter count if a seat is free
        return count