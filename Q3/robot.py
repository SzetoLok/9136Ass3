from geo_features import *

class Robot:
    """
    Represents Robbie the Explorer on a toroidal Mars map.
    Handles movement, exploration, and journey logging.

    Instance Variables:
        current_location (Location): Robbie's current position on the map.
        map_size (Size): The dimensions of the map.
        journey_log (list): List of tuples (start_day, end_day, action_str) recording Robbie's actions.
        current_day (int): The current day in Robbie's journey.
        exploration_speeds (dict): Exploration speed for each feature type.
    """

    def __init__(self, map_size) -> None:
        """
        Initialize the robot at (0, 0) with the given map size.

        Arguments:
            map_size (Size): The dimensions of the Mars map.
        """

        self.current_location = Location(0, 0)  # Start at the top-left corner
        self.map_size = map_size                # Store the map size
        self.journey_log = []                   # Initialize the journey log
        self.current_day = 1                    # Start at day 1
        self.exploration_speeds = {             # Initial exploration speeds
            'mountain': 6.0,
            'lake': 8.0,
            'crater': 10.0
        }


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


    def move_to(self, target_location: Location) -> tuple:
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


    def explore_feature(self, feature: object) -> int:
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
        speed = self.exploration_speeds[feature_type]

        # If the feature value is not perfectly divisible by speed, use ceiling division
        if feature_value % speed != 0:
            days_needed = int(-(-feature_value // speed))
        else:
            # If perfectly divisible, use normal division
            days_needed = int(feature_value // speed)

        # Increase the exploration speed for this feature type by 20%
        self.exploration_speeds[feature_type] *= 1.2

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
        feature_name_list: list[str],
        geological_feature_location_dictionary: dict,
        starting_location: Location = None,
        starting_exploration_boosts: dict = None,
        form_exploration_speeds: dict = None
    ) -> tuple[int, list]:
        """
        Simulate a mission for a given list of feature names and robot form,
        returning the total days required and the step-by-step plan.
        Does not alter the real robot's state.

        Arguments:
            feature_name_list (list[str]): List of feature names (str) to explore, in order.
            geological_feature_location_dictionary (dict): Dictionary mapping (row, col) to feature objects.
            starting_location (Location, optional): Where to start the mission. If None, uses current_location.
            starting_exploration_boosts (dict, optional): Speed boost factors for each feature type. If None, uses current boosts.
            form_exploration_speeds (dict, optional): Base exploration speeds for the chosen form. If None, uses current form's speeds.

        Returns:
            tuple: (total_days (int), plan (list))
                total_days: Total number of days required to complete the mission.
                plan: List of tuples, each tuple is
                    (move_path (list of Location), feature, move_days (int), explore_days (int))
        """
        # Use provided or current state for simulation
        if starting_location is None:
            simulation_location = Location(self.current_location.Y, self.current_location.X)
        else:
            simulation_location = Location(starting_location.Y, starting_location.X)

        if starting_exploration_boosts is None:
            simulation_exploration_boosts = self.exploration_boosts.copy() if hasattr(self, 'exploration_boosts') else {'mountain': 1.0, 'lake': 1.0, 'crater': 1.0}
        else:
            simulation_exploration_boosts = starting_exploration_boosts.copy()

        if form_exploration_speeds is None:
            # Use current form's base speeds if not provided
            simulation_base_speeds = self.exploration_speeds.copy()
        else:
            simulation_base_speeds = form_exploration_speeds.copy()

        total_days = 0
        plan = []

        # Build a mapping from feature name to feature object for quick lookup
        feature_name_to_object = {feature.name: feature for feature in geological_feature_location_dictionary.values()}

        for feature_name in feature_name_list:
            feature = feature_name_to_object[feature_name]

            # Simulate movement to the feature
            move_path, move_days = self._simulate_move(simulation_location, feature.location)

            # Simulate exploration of the feature
            feature_type = feature.feature_type
            feature_value = feature.feature_value[1]
            # Calculate current effective speed for this feature type
            current_speed = simulation_base_speeds[feature_type] * simulation_exploration_boosts[feature_type]
            # Use ceiling division for days (always round up)
            explore_days = -(-feature_value // current_speed) if feature_value % current_speed != 0 else feature_value // current_speed
            explore_days = int(explore_days)

            # Update boosts for next feature
            simulation_exploration_boosts[feature_type] *= 1.2

            # Update location and total days
            simulation_location = feature.location
            total_days += move_days + explore_days

            # Add this step to the plan
            plan.append((move_path, feature, move_days, explore_days))

        return total_days, plan

    def _simulate_move(self, start_location: Location, end_location: Location) -> tuple[list, int]:
        """
        Simulate movement from start_location to end_location, returning (path, days).
        Does not alter the robot's state.

        Arguments:
            start_location (Location): Starting location.
            end_location (Location): Ending location.

        Returns:
            tuple: (path (list of Location), days (int))
        """
        path = [Location(start_location.Y, start_location.X)]
        current_row_index, current_column_index = start_location.Y, start_location.X
        target_row_index, target_column_index = end_location.Y, end_location.X

        # Move horizontally first
        horizontal_path, new_column_index = self._move_along_axis(
            current=current_column_index,
            target=target_column_index,
            size=self.map_size.width,
            axis='x',
            fixed_coord=current_row_index
        )
        path.extend(horizontal_path)

        # Move vertically next
        vertical_path, new_row_index = self._move_along_axis(
            current=current_row_index,
            target=target_row_index,
            size=self.map_size.height,
            axis='y',
            fixed_coord=new_column_index
        )
        path.extend(vertical_path)

        return path, len(path) - 1
