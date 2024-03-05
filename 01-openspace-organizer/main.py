from src.openspace import OpenSpace

if __name__ == "__main__":
 
    def main():
        path = input("Please enter the path to file: ")
        with open(path, "r") as file:
            lines = file.readlines()
            colleagues = []
            for line in lines:
                new_line = line.rstrip("\n")
                colleagues.append(new_line)
        # Create an OpenSpace object
            open_space = OpenSpace()

        # Organize the colleagues
            open_space.organize(colleagues)

        # Display the repartition
            open_space.display()

        # Store the repartition
            open_space.store()