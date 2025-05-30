from Q2.geo_features import Location, Size, Mountain, Lake, Crater

def load_geological_features(file_name):
    
    geological_feature_location_dictionary = {}

    with open(file_name, "r") as file:
        file_lines = file.readlines()

    first_line = file_lines[0].strip().split(",")
    number_of_rows = int(first_line[0])
    number_of_columns = int(first_line[1])

    map_size = Size(number_of_rows, number_of_columns)

    for line in file_lines[1:]:
        feature_parts = line.strip().split(",")
        row_index = int(feature_parts[0].strip())
        column_index = int(feature_parts[1].strip())
        feature_type = feature_parts[2].strip()
        feature_name = feature_parts[3].strip()
        feature_value = int(feature_parts[4].strip())
        feature_location = Location(row_index, column_index)

        if feature_type == "mountain":
            geological_feature = Mountain(feature_location, feature_name, feature_value)
        elif feature_type == "lake":
            geological_feature = Lake(feature_location, feature_name, feature_value)
        elif feature_type == "crater":
            geological_feature = Crater(feature_location, feature_name, feature_value)
        else:
            continue

        geological_feature_location_dictionary[(row_index, column_index)] = geological_feature

    return map_size, geological_feature_location_dictionary

def display_map(map_size, geological_feature_location_dictionary):

    grid = []
    for row_index in range(map_size.height):
        map_row = ""

        for column_index in range(map_size.width):

            geological_feature = geological_feature_location_dictionary.get((row_index, column_index))

            if geological_feature is None:
                map_row += "."
            else:
                map_row += geological_feature.symbol()
        grid.append(map_row)
    
    for row in grid:
        print(row)

def main():
    map_size, geological_feature_location_dictionary = load_geological_features("Q1/geo_features.txt")

    exit_is_found = False
    while not exit_is_found:

        user_input = input("> ").strip()

        if user_input == "quit":
            print("goodbye")
            exit_is_found = True

        elif user_input == "show map":
            display_map(map_size, geological_feature_location_dictionary)

        elif user_input.startswith("info "):

                _, row_string, column_string = user_input.split()
                row_index = int(row_string)
                column_index = int(column_string)

                geological_feature = geological_feature_location_dictionary.get((row_index, column_index))
                
                if geological_feature:
                    print(geological_feature)
                else:
                    print("no information found")

        else:
            print("no information found")

if __name__ == "__main__":
    main()
