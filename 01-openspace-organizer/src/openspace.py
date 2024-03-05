#### 2. An open space
import openpyxl, os, random
from src.table import Table, Seat

class OpenSpace:
    def __init__(self, number_of_tables: int = 6) -> None:
        self.number_of_tables = number_of_tables
        self.tables = [Table() for _ in range(number_of_tables)]

#Add some methods:
# `organize(names)` that will **randomly** assign people to the `Seat` objects in the different `Table` objects
    def organize(self, names: list):
        """
        Randomly assign people to seats in the open space.
        Prefer tables with more than one person already.
        """
        print(f"\nTotal people: {len(names)}")
        # Randomize the order of names
        random.shuffle(names)
        # Check if capacity is enough
        total_capacity = sum(table.capacity for table in self.tables)
        if len(names) > total_capacity:
            print(f"\nMissing {len(names)-total_capacity} seats")
            print(f"\nUnseated people: {names[total_capacity:]}")
        # Assign people to tables one by one
        unseated = []
        while names:
            for table in self.tables:
                if table.has_free_spot():
                    table.assign_seat(names.pop())

            # Check if all tables are full
            if all(not table.has_free_spot() for table in self.tables):
                # Assign remaining people to the open space
                unseated.extend(names)
                break
        return unseated

# `display()` to display the different tables and their occupants in a nice and readable way
    def display(self) -> (int, int, int):
        total_capacity = sum(table.capacity for table in self.tables)
        seats_left = 0

        for table in self.tables:
            seats_left += table.capacity_left()

    # Display table information and additional stats
        for i, table in enumerate(self.tables):
            table_name = f"Table {i + 1}"
            occupied_seats = [seat.occupant for seat in table.seats if seat.free is False]

            if occupied_seats:
                print(f"\n{table_name}:")
                for occupant in occupied_seats:
                    print(f"* {occupant}")

        print(f"\nTotal capacity: {total_capacity}")
        print(f"\nSeats left: {seats_left}")

        return total_capacity, seats_left

# `store(filename)` to store the repartition in an Excel file
    def store(self, filename: str = "results_organizer.xlsx") -> None:
        """
        Store the repartition of people in the open space in an Excel file
        """
        # Construct the path to the desktop directory
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        # Create a worksheet
        ws = wb.active
        # Write the header row
        ws.append(["Table", "Name"])

        # Iterate over tables and add table data to the worksheet
        for i, table in enumerate(self.tables):
            for i, seat in enumerate(table.seats):
                if seat.free is False:
                    ws.append([i + 1, seat.occupant])

        # Save the workbook to the desktop directory
        cwd = os.getcwd()
        wb.save(os.path.join(cwd, filename))