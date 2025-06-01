from geo_features import *

class BaseRobot:
    """
    Base class for all robot forms. Handles common logic for movement, exploration, and journey logging.
    """
    FORM_SPEEDS = {}  # Overridden by subclasses

    def __init__(self, map_size, current_location, journey_log, current_day, exploration_boosts):
        self.map_size = map_size
        self.current_location = current_location
        self.journey_log = journey_log
        self.current_day = current_day
        self.exploration_boosts = exploration_boosts
        self.exploration_speeds = self._get_current_speeds()

    def _get_current_speeds(self):
        return {feature_type: self.FORM_SPEEDS[feature_type] * self.exploration_boosts[feature_type] 
                for feature_type in self.FORM_SPEEDS}

    def move_to(self, target_location: Location, suppress_output: bool = False) -> None:
        """
        Moves Robbie to the specified target location on the map, always prioritizing horizontal movement first
        (with wrap-around if optimal), then vertical movement. The function returns the path Robbie takes and
        the number of days required for the move. If Robbie is already at the target location, no movement is performed.

        Arguments:
            target_location (Location): The destination location Robbie should move to.

        Returns:
            None
        """

        # Calculate the path and days needed to reach the target location
        path, days = self.calculate_path(target_location)

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
            if not suppress_output:
                print(f"move from {path[0]} to {path[-1]}")

            # Log the movement in the robot's journey log
            self.log_action(self.current_day, self.current_day + days - 1, f"move {move_string}")

            # Update the current day
            self.current_day += days


    def calculate_path(self, target_location: Location) -> tuple:
        """
        Move to the target location, prioritizing horizontal movement and wrapping if optimal.

        Args:
            target_location (Location): The destination location.

        Returns:
            tuple: (path (list of Location), days_needed (int))
                path: List of visited locations (including start and end).
                days_needed: Number of days required to reach the destination.
                Returns (None, 0) if already at the target location.
        """

        # If already at the target, do nothing and return immediately
        if self.current_location == target_location:
            return None, 0

        # Start path with current location
        path = [self.current_location]  
        current_y = self.current_location.Y
        current_x = self.current_location.X
        target_y = target_location.Y
        target_x = target_location.X

        # Move horizontally first (X axis)
        x_path, new_x = self._move_along_axis(current_x, target_x, self.map_size.width, 'x', current_y)
        path.extend(x_path)

        # Move vertically next (Y axis)
        y_path, new_y = self._move_along_axis(current_y, target_y, self.map_size.height, 'y', new_x)
        path.extend(y_path)

        # Update current location to new position
        self.current_location = Location(new_y, new_x)

        return path, len(path) - 1


    def _move_along_axis(
        self,
        current_coordinate: int,
        target_coordinate: int,
        map_size: int,
        axis: str,
        fixed_coordinate: int
    ) -> tuple[list, int]:
        """
        Move along a single axis (horizontal or vertical), preferring minimal steps,
        and if tied, preferring the wrapping direction.

        Args:
            current_coordinate (int): Current coordinate (row or column).
            target_coordinate (int): Target coordinate (row or column).
            map_size (int): Size of the axis (width or height).
            axis (str): 'x' for horizontal, 'y' for vertical.
            fixed_coordinate (int): The coordinate that stays fixed (row for x, column for y).

        Returns:
            tuple: (path (list of Location), final_coordinate (int))
                path: Locations visited (excluding starting location).
                final_coordinate: Final coordinate after movement.
        """
        
        # Calculates the number of steps needed to move from the current coordinate to the target coordinate by 
        # incrementing (moving "forward" or "right/down" along the axis), wrapping around the grid if necessary.
        steps_positive = (target_coordinate - current_coordinate) % map_size

        # Calculates the number of steps needed to move from the current coordinate to the target coordinate by 
        # decrementing (moving "backward" or "left/up" along the axis), wrapping around the grid if necessary.
        steps_negative = (current_coordinate - target_coordinate) % map_size
        path = []

        # If moving in the positive direction is shorter, then move in positive direction
        if steps_positive < steps_negative:
            direction = 1
            steps = steps_positive

        # If moving in the negative direction is shorter, then move in negative direction
        elif steps_negative < steps_positive:
            direction = -1
            steps = steps_negative

        else:
        # If both directions (positive and negative) require the same number of steps,
        # we need to pick the path that actually wraps around the grid boundary.
        # To do this, we check the relationship between target_coordinate and current_coordinate:
        # - If target_coordinate > current_coordinate, moving in the negative direction (decreasing index)
        #   will wrap around the grid boundary to reach the target.
        # - If target_coordinate < current_coordinate, moving in the positive direction (increasing index)
        #   will wrap around the grid boundary to reach the target.
        # This ensures that, in the case of a tie, we always prefer the movement that wraps.

            # Moving in the negative direction (decreasing index) will wrap around the grid.
            if target_coordinate > current_coordinate:
                direction = -1 

            # Moving in the positive direction (increasing index) will wrap around the grid.    
            else:
                direction = 1

            # The number of steps is the same for both directions in a tie.
            steps = steps_positive

        # Build the path for each step
        for step in range(1, steps + 1):

            # Calculate the new coordinate after moving one step in the chosen direction and wrap around if needed
            new_coordinate = (current_coordinate + direction * step) % map_size

            # If moving along the X axis, create a Location with the fixed row and new column
            if axis == 'x':
                location = Location(fixed_coordinate, new_coordinate)

            # If moving along the Y axis, create a Location with the new row and fixed column
            else:
                location = Location(new_coordinate, fixed_coordinate)

            # Add the new location to the path
            path.append(location)

        # After completing all steps, compute the final coordinate after movement and wrap around if needed
        final_coordinate = (current_coordinate + direction * steps) % map_size
        return path, final_coordinate


    def explore_feature(self, feature: object, suppress_output: bool = False) -> None:
        """
        Explores the geological feature at Robbie's current location. The time required depends on
        Robbie's current exploration speed for the feature type and the feature's size. After each
        exploration, Robbie's speed for that feature type increases by 20%. If there is no feature
        at the current location, nothing happens.

        Arguments:
            feature (object): The geological feature to explore (Mountain, Lake, or Crater).

        Returns:
            None
        """

        # Calculate the days required to explore the feature
        days = self.calculate_days_required(feature)

        # If there is nothing to explore
        if days == 0:
            print("nothing to explore")

        # If there is a feature to explore    
        else:
            if not suppress_output:
                print(f"explore {feature.feature_type} {feature.name}")

            # Log the exploration in the robot's journey log
            self.log_action(self.current_day, self.current_day + days - 1, f"explore {feature.feature_type} {feature.name}")
            
            # Update the current day
            self.current_day += days


    def calculate_days_required(self, feature: object) -> int:
        """
        Calculates the number of days required for Robbie to explore the given feature,
        updates the exploration speed for the feature type by increasing it by 20% after each exploration,
        and returns the number of days needed.

        Args:
            feature (object): The geological feature to explore (Mountain, Lake, or Crater).

        Returns:
            int: The number of days required to explore the feature.
                 Returns 0 if there is no feature at the current location.
        """

        # If there is no feature at the current location, do nothing and return 0
        if not feature:
            return 0

        # Get the feature type string from the feature
        feature_type = feature.feature_type
        # Get the feature value for exploration (height, depth, or perimeter)
        feature_value = feature.feature_value[1]
        # speed = self.exploration_speeds[feature_type]
        speed = self.FORM_SPEEDS[feature_type] * self.exploration_boosts[feature_type]

        # If the feature value is not perfectly divisible by speed, use ceiling division
        if feature_value % speed != 0:
            days_needed = int(-(-feature_value // speed))
        else:
            # If perfectly divisible, use normal division
            days_needed = int(feature_value // speed)

        # Increase the exploration speed for this feature type by 20%
        self.exploration_boosts[feature_type] *= 1.2

        # print(f'speed: {speed}, days_needed: {days_needed}')
        # Return the number of days needed to explore the feature
        return days_needed


    def log_action(self, start_day: int, end_day: int, action_str: str) -> None:
        """
        Log an action to the journey log.

        Args:
            start_day (int): The starting day of the action.
            end_day (int): The ending day of the action.
            action_str (str): The action description.

        Returns:
            None
        """

        # Add the action to the journey log
        self.journey_log.append((start_day, end_day, action_str))


    def display_journey(self) -> None:
        """
        Print the journey log in the required format.

        Returns:
            None
        """

        # If an empty journey needs to be displayed, print a blank line
        if len(self.journey_log) == 0:
            print()

        for start, end, action in self.journey_log:

            # If the action occurred on a single day
            if start == end:
                print(f"Day {start}: {action}")

            else:
                # If the action spanned multiple days
                print(f"Day {start}-{end}: {action}")


    def simulate_mission(
                        self,
                        feature_name_list: list,
                        geological_feature_location_dictionary: dict
                        ) -> int:
        """
        Simulate a mission for the current robot form, starting from the robot's current state.
        Returns the total number of days required to complete all explorations (ignoring travel time).
        This method does NOT modify the real robot's state.

        Arguments:
            feature_name_list (list): List of feature names (str) to explore, in order.
            geological_feature_location_dictionary (dict): Dictionary mapping (row, col) to feature objects.

        Returns:
            int: Total number of days required to complete the mission (exploration only).
        """

        # Copy the robot's current exploration boosts for simulation
        simulated_exploration_boosts = self.exploration_boosts.copy()
        total_exploration_days = 0

        # Build a mapping from feature name to feature object for quick lookup
        feature_name_to_object = {feature.name: feature for feature in geological_feature_location_dictionary.values()}

        for feature_name in feature_name_list:
            feature = feature_name_to_object[feature_name]

            # Get the feature type and value
            feature_type = feature.feature_type
            feature_value = feature.feature_value[1]

            # Calculate the current effective speed for this feature type
            current_speed = self.FORM_SPEEDS[feature_type] * simulated_exploration_boosts[feature_type]

            # print(f'{type(self)} current_speed: {current_speed} for {feature_type}')
            # Calculate the number of days needed to explore (always round up)
            if feature_value % current_speed != 0:
                explore_days = int(-(-feature_value // current_speed))
            else:
                explore_days = int(feature_value // current_speed)


            # Add to the total exploration days
            total_exploration_days += explore_days

            # Update the boost for this feature type for the next exploration
            simulated_exploration_boosts[feature_type] *= 1.2

        return total_exploration_days



class Robot(BaseRobot):
    """Default robot form"""
    def __init__(self, map_size, current_location, journey_log, current_day, exploration_boosts):
        super().__init__(map_size, current_location, journey_log, current_day, exploration_boosts)
        self.FORM_SPEEDS = {'mountain': 6.0, 'lake': 8.0, 'crater': 10.0}


class Drone(BaseRobot):
    """Drone form with different exploration speeds"""
    def __init__(self, map_size, current_location, journey_log, current_day, exploration_boosts):
        super().__init__(map_size, current_location, journey_log, current_day, exploration_boosts)
        self.FORM_SPEEDS = {'mountain': 12.0, 'lake': 6.0, 'crater': 8.0}


class AUV(BaseRobot):
    """AUV form with different exploration speeds"""
    def __init__(self, map_size, current_location, journey_log, current_day, exploration_boosts):
        super().__init__(map_size, current_location, journey_log, current_day, exploration_boosts)
        self.FORM_SPEEDS = {'mountain': 2.0, 'lake': 12.0, 'crater': 6.0}


class Transformer:
    """Manages robot transformations while preserving state"""

    def __init__(self, map_size):
        self.robot = Robot(
            map_size=map_size,
            current_location=Location(0, 0),
            journey_log=[],
            current_day=1,
            exploration_boosts={'mountain': 1.0, 'lake': 1.0, 'crater': 1.0}
        )

    def transform(self, new_form: str):
        """Transform into a new form (robot/drone/auv)"""
        if new_form == "robot":
            class_type = Robot
        elif new_form == "drone":
            class_type = Drone
        elif new_form == "auv":
            class_type = AUV
        else:
            raise ValueError("Invalid form")

        # Preserve all state during transformation
        self.robot = class_type(
            map_size=self.robot.map_size,
            current_location=self.robot.current_location,
            journey_log=self.robot.journey_log,
            current_day=self.robot.current_day,
            exploration_boosts=self.robot.exploration_boosts
        )

    def run_mission(self, feature_names: list[str], geological_feature_location_dictionary: dict) -> None:
            """
            Determines the best form for the mission, transforms, and executes the mission.
            Handles all state updates, printing, and journey logging.

            Args:
                feature_names (list[str]): List of feature names to explore in order.
                geological_feature_location_dictionary (dict): Map from (row, col) to feature objects.

            Returns:
                None
            """

            # Preference order: robot > drone > auv
            best_form = "robot"
            best_days = float('inf')

            for form in ["robot", "drone", "auv"]:
                self.transform(form)
                days = self.robot.simulate_mission(feature_names, geological_feature_location_dictionary)
                if days < best_days or (days == best_days and ["robot", "drone", "auv"].index(form) < ["robot", "drone", "auv"].index(best_form)):
                    best_days = days
                    best_form = form

            # Transform into the chosen form for the mission
            self.transform(best_form)

            if best_form == "robot":
                print("no transformation")

            elif best_form == "auv":
                print(f"transform into an {best_form.upper()}")

            elif best_form == "drone":
                print(f"transform into a {best_form}")


            # Build a mapping from feature name to feature object for quick lookup
            feature_name_to_object = {feature.name: feature for feature in geological_feature_location_dictionary.values()}

            for feature_name in feature_names:
                feature = feature_name_to_object[feature_name]
                start_location = self.robot.current_location
                end_location = feature.location

                # Check if already at the feature location
                if start_location == end_location:
                    # Already at the location: print "same location, explore ..."
                    print(f"same location, explore {feature.feature_type} {feature.name}")
                else:
                    # Need to move: print "move from ... to ... then explore ..."
                    print(f"move from {start_location} to {end_location} then explore {feature.feature_type} {feature.name}")
                    self.robot.move_to(end_location, suppress_output=True)  # Move the robot (updates location and journey log)

                # Explore the feature (updates boosts and journey log, but suppress internal print)
                self.robot.explore_feature(feature, suppress_output=True)

            # After the mission, always revert to regular robot form
            self.transform("robot")
