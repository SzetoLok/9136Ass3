from Q2.geo_features import Location

class Robot:
    """
    Represents Robbie the Explorer on a toroidal Mars map.
    Handles movement, exploration, and journey logging.
    """
    def __init__(self, map_size):
        """
        Initialize the robot at (0, 0) with the given map size.
        """
        self.current_location = Location(0, 0)
        self.map_size = map_size
        self.journey_log = []
        self.current_day = 1
        self.exploration_speeds = {
            'mountain': 6.0,
            'lake': 8.0,
            'crater': 10.0
        }
        self.exploration_counts = {'mountain': 0, 'lake': 0, 'crater': 0}

    def move_to(self, target_location):
        """
        Move to the target location, prioritizing horizontal movement.
        Returns the list of locations visited (including start and end).
        """
        path = [Location(self.current_location.Y, self.current_location.X)]
        y = self.current_location.Y
        x = self.current_location.X
        target_y = target_location.Y
        target_x = target_location.X
        width = self.map_size.width
        height = self.map_size.height

        # Horizontal movement first
        direct_x = (target_x - x) % width
        wrap_x = (x - target_x) % width
        if direct_x <= wrap_x:
            for _ in range(direct_x):
                x = (x + 1) % width
                path.append(Location(y, x))
        else:
            for _ in range(wrap_x):
                x = (x - 1) % width
                path.append(Location(y, x))

        # Then vertical movement
        direct_y = (target_y - y) % height
        wrap_y = (y - target_y) % height
        if direct_y <= wrap_y:
            for _ in range(direct_y):
                y = (y + 1) % height
                path.append(Location(y, x))
        else:
            for _ in range(wrap_y):
                y = (y - 1) % height
                path.append(Location(y, x))

        self.current_location = Location(y, x)
        return path

    def explore_feature(self, feature):
        """Calculate exploration time and update speeds"""
        if not feature:
            return 0
            
        explore_type = type(feature)
        days_needed = self._calculate_exploration_days(feature)
        
        # Apply speed boost after exploration
        if feature not in self.explored_features:
            self.exploration_speeds[explore_type] *= 1.2
            self.explored_features.add(feature)
            
        return days_needed

    def _calculate_exploration_days(self, feature):
        """Calculate days needed with ceiling"""
        if isinstance(feature, Mountain):
            size = feature.height
        elif isinstance(feature, Lake):
            size = feature.depth
        else:
            size = feature.perimeter
            
        speed = self.exploration_speeds[type(feature)]
        return (size / speed).__ceil__()

    def move_to(self, target_location):
        """
        Move to the target location, prioritizing horizontal movement.
        Returns the list of locations visited (including start and end).
        """
        path = [Location(self.current_location.Y, self.current_location.X)]
        y = self.current_location.Y
        x = self.current_location.X
        target_y = target_location.Y
        target_x = target_location.X

        # 1. Move horizontally first (X axis)
        x_path, x = self._move_horizontal(x, target_x, y)
        path.extend(x_path)

        # 2. Then move vertically (Y axis)
        y_path, y = self._move_vertical(y, target_y, x)
        path.extend(y_path)

        self.current_location = Location(y, x)
        return path

    def _move_horizontal(self, current_x, target_x, y):
        """
        Move horizontally from current_x to target_x on row y.
        Returns the path (excluding the starting location) and the final x.
        """
        width = self.map_size.width
        # Calculate direct and wrap distances
        direct = (target_x - current_x) % width
        wrap = (current_x - target_x) % width
        path = []
        if direct <= wrap:
            # Move right
            for step in range(1, direct + 1):
                new_x = (current_x + step) % width
                path.append(Location(y, new_x))
            final_x = (current_x + direct) % width
        else:
            # Move left (wrap)
            for step in range(1, wrap + 1):
                new_x = (current_x - step) % width
                path.append(Location(y, new_x))
            final_x = (current_x - wrap) % width
        return path, final_x

    def _move_vertical(self, current_y, target_y, x):
        """
        Move vertically from current_y to target_y in column x.
        Returns the path (excluding the starting location) and the final y.
        """
        height = self.map_size.height
        direct = (target_y - current_y) % height
        wrap = (current_y - target_y) % height
        path = []
        if direct <= wrap:
            # Move down
            for step in range(1, direct + 1):
                new_y = (current_y + step) % height
                path.append(Location(new_y, x))
            final_y = (current_y + direct) % height
        else:
            # Move up (wrap)
            for step in range(1, wrap + 1):
                new_y = (current_y - step) % height
                path.append(Location(new_y, x))
            final_y = (current_y - wrap) % height
        return path, final_y