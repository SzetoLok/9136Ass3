"""
This program loads a Mars map from a file, displays the map, and allows the user to
query information about geological features (mountain, lake, crater) at any location.
It uses the feature classes defined in geo_features.py and provides an interactive
command-line interface for map exploration.

Author : Szeto Lok
"""

from geo_features import Location, Size, Mountain, Lake, Crater
from robot import *

def load_geological_features(file_name: str) -> tuple:
    """
    Loads the map size and geological features from a file.

    Arguments:
        file_name (str): The name of the file containing map and feature data.

    Returns:
        tuple: (map_size (Size), geological_feature_location_dictionary (dict))
            map_size: The size of the map.
            geological_feature_location_dictionary: A dictionary mapping (row_index, column_index) to feature objects.
    """

    # Dictionary to hold features by their coordinates
    geological_feature_location_dictionary = {}

    # Open the file and read all lines
    with open(file_name, "r") as file:
        file_lines = file.readlines()

    # Parse the first line to get map dimensions
    first_line = file_lines[0].strip().split(",")
    number_of_rows = int(first_line[0])
    number_of_columns = int(first_line[1])

    # Create Size object for the map
    map_size = Size(number_of_rows, number_of_columns)

    # Iterate over each feature line (skip the first line)
    for line in file_lines[1:]:

        # Split line into parts for each feature attribute
        feature_parts = line.strip().split(",")
        row_index = int(feature_parts[0].strip())
        column_index = int(feature_parts[1].strip())
        feature_type = feature_parts[2].strip()
        feature_name = feature_parts[3].strip()
        feature_value = int(feature_parts[4].strip())
        feature_location = Location(row_index, column_index)

        # Instantiate the correct feature class based on type
        if feature_type == "mountain":
            geological_feature = Mountain(feature_location, feature_name, feature_type, feature_value)

        elif feature_type == "lake":
            geological_feature = Lake(feature_location, feature_name, feature_type, feature_value)

        elif feature_type == "crater":
            geological_feature = Crater(feature_location, feature_name, feature_type, feature_value)

        else:
            # Skip unknown feature types
            continue

        # Store feature in dictionary with its coordinates as key
        geological_feature_location_dictionary[(row_index, column_index)] = geological_feature

    # Return map size and feature dictionary
    return map_size, geological_feature_location_dictionary


def display_map(map_size: Size, geological_feature_location_dictionary: dict) -> None:
    """
    Prints the map using symbols for each geological feature.

    Arguments:
        map_size (Size): The size of the map.
        geological_feature_location_dictionary (dict): Dictionary mapping locations to features.

    Returns:
        None
    """

    # List to store each row of the map as a string
    grid = []

    # Loop through each row of the map
    for row_index in range(map_size.height):

        # Start with an empty row string
        map_row = ""

        # Loop through each column of the map
        for column_index in range(map_size.width):

            # Look up the feature at this location (if any)
            geological_feature = geological_feature_location_dictionary.get((row_index, column_index))

            if geological_feature is None:

                # Add '.' if no feature at this location
                map_row += "."

            else:

                # Add the feature's symbol if present
                map_row += geological_feature.symbol()

        # Add the row string to the grid
        grid.append(map_row)

    # Print each row of the map
    for row in grid:
        print(row)


def main() -> None:
    """
    Runs the user interaction loop for Robbie the Explorer.

    Commands:
        show map: Displays the map.
        info <Y> <X>: Shows details about the feature at (Y, X).
        moveto <Y> <X>: Move Robbie to a new location.
        explore: Explore the current location.
        display journey: Show Robbie's journey log.
        quit: Exits the program.

    Returns:
        None
    """

    # Load map size and features from file
    map_size, geological_feature_location_dictionary = load_geological_features("Q2/geo_features.txt")

    # Create the robot instance
    robot = Robot(map_size)

    # Flag to control loop exit
    exit_is_found = False

    # Main user input loop
    while not exit_is_found:

        # Prompt user for input and remove leading/trailing whitespace
        user_input = input("> ").strip()

        # If user wants to quit
        if user_input == "quit":
            print("goodbye")
            exit_is_found = True

        # If user wants to display the map
        elif user_input == "show map":
            display_map(map_size, geological_feature_location_dictionary)

        # If user wants information about a specific location
        elif user_input.startswith("info "):

            # Parse the info command to get coordinates
            _, row_string, column_string = user_input.split()
            row_index = int(row_string)
            column_index = int(column_string)

            # Look up the feature at the given coordinates
            geological_feature = geological_feature_location_dictionary.get((row_index, column_index))

            # If there a feature is found, print it
            if geological_feature:
                print(geological_feature)

            else:
                print("no information found")

        # If user wants to move Robbie to a new location
        elif user_input.startswith("moveto "):

            # Parse the moveto command to get coordinates
            _, row_string, column_string = user_input.split()
            row_index = int(row_string)
            column_index = int(column_string)
            target_location = Location(row_index, column_index)

            # Move the robot and get the path and days needed
            path, days = robot.move_to(target_location)

            # If already at the target location
            if path is None:
                print("same location")

            else:
                # Build the move string step by step
                move_string = ""

                for index, location in enumerate(path):

                    if index == 0:

                        # Add the first location without an arrow
                        move_string += str(location)

                    else:

                        # Add subsequent locations with arrows
                        move_string += " -> " + str(location)

                # Print the move summary
                print(f"move from {path[0]} to {path[-1]}")

                # Log the movement in the robot's journey log
                robot.log_action(robot.current_day, robot.current_day + days - 1, f"move {move_string}")

                # Update the current day
                robot.current_day += days

        # If user wants Robbie to explore the current location
        elif user_input == "explore":

            # Get the current location as a tuple
            current = (robot.current_location.Y, robot.current_location.X)

            # Get the feature at the current location
            feature = geological_feature_location_dictionary.get(current)

            # Explore the feature and get the days needed
            days = robot.explore_feature(feature)

            # If there is nothing to explore
            if days == 0:
                print("nothing to explore")

            # If there is a feature to explore    
            else:
                print(f"explore {feature.feature_type} {feature.name}")

                # Log the exploration in the robot's journey log
                robot.log_action(robot.current_day, robot.current_day + days - 1, f"explore {feature.feature_type} {feature.name}")
                
                # Update the current day
                robot.current_day += days

        # If user wants to display the journey log
        elif user_input == "display journey":
            robot.display_journey()

        # If the command is not recognized
        else:
            print("no information found")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()