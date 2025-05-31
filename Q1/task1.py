"""
This program loads a Mars map from a file, displays the map, and allows the user to
query information about geological features (mountain, lake, crater) at any location.
It uses the feature classes defined in geo_features.py and provides an interactive
command-line interface for map exploration.

Author : Szeto Lok
"""

from geo_features import Location, Size, Mountain, Lake, Crater

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
    Runs the user interaction loop for Robbie the Map Reader.

    Commands:
        show map: Displays the map.
        info <Y> <X>: Shows details about the feature at (Y, X).
        quit: Exits the program.

    Returns:
        None
    """

    # Load map size and features from file
    map_size, geological_feature_location_dictionary = load_geological_features("Q1/geo_features.txt")

    # Flag to control loop exit
    exit_is_found = False 

    # Main user input loop
    while not exit_is_found:

        # Prompt user for input and remove leading/trailing whitespace
        user_input = input("> ").strip()

        if user_input == "quit":

            # Print goodbye and exit the loop
            print("goodbye")
            exit_is_found = True

        elif user_input == "show map":

            # Display the map to the user
            display_map(map_size, geological_feature_location_dictionary)

        elif user_input.startswith("info "):

            # Parse the info command to get coordinates
            _, row_string, column_string = user_input.split()
            row_index = int(row_string)
            column_index = int(column_string)

            # Look up the feature at the given coordinates
            geological_feature = geological_feature_location_dictionary.get((row_index, column_index))
            
            if geological_feature:

                # Print feature details (calls __str__)
                print(geological_feature)

            else:

                # No feature found at this location
                print("no information found")

        else:
            
            # Command not recognized
            print("no information found")

if __name__ == "__main__":
    main()
