from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Location:
    """
    Location class for representing coordinates on the map.

    Instance Variables:
        Y (int): The row index (0-based).
        X (int): The column index (0-based).
    """

    Y: int = 0
    X: int = 0


    def __str__(self) -> str:
        """
        Returns the string representation of the location.

        Returns:
            str: The location in the format '(Y,X)'.
        """

        # Format the location as (Y,X)
        return f"({self.Y},{self.X})"


@dataclass
class Size:
    """
    Size class for representing the dimensions of the map.

    Instance Variables:
        height (int): The number of rows in the map.
        width (int): The number of columns in the map.
    """

    height: int = 0
    width: int = 0


class GeoFeature(ABC):
    """
    Abstract base class for geological features.

    Instance Variables:
        location (Location): The location of the feature on the map.
        name (str): The name of the geological feature.
    """

    def __init__(self, location: Location, name: str) -> None:
        """
        Initializes a geological feature.

        Arguments:
            location (Location): The location of the feature.
            name (str): The name of the feature.
        """

        # Store the feature's location and name
        self.location = location
        self.name = name


    @abstractmethod
    def symbol(self) -> str:
        """
        Returns a single-character symbol representing the feature.

        Returns:
            str: The symbol for the feature.
        """
        pass


    def __str__(self) -> str:
        """
        Returns a string with detailed information about the feature.

        Returns:
            str: The detailed information.
        """
        
        # Return the formatted string for the lake
        return f"{self.feature_type} {self.name}, {self.feature_value[0]} {self.feature_value[1]}"


class Mountain(GeoFeature):
    """
    Mountain class for representing mountain features.

    Instance Variables:
        feature_type (str): The type of the feature ("mountain").
        feature_value (list): A list where feature_value[0] is the string 'height' and feature_value[1] is the numeric height.
    """

    def __init__(self, location: Location, name: str, feature_type: str, height: int) -> None:
        """
        Initializes a Mountain instance.

        Arguments:
            location (Location): The location of the mountain.
            name (str): The name of the mountain.
            feature_type (str): The type of the feature ("mountain").
            height (int): The height of the mountain.
        """

        # Call the base class constructor
        super().__init__(location, name)

        # Store the feature type and value as a list
        self.feature_type = feature_type
        self.feature_value = ['height', height]


    def symbol(self) -> str:
        """
        Returns the symbol for a mountain.

        Returns:
            str: 'm'
        """

        # Return 'm' for mountain
        return 'm'


class Lake(GeoFeature):
    """
    Lake class for representing lake features.

    Instance Variables:
        feature_type (str): The type of the feature ("lake").
        feature_value (list): A list where feature_value[0] is the string 'depth' and feature_value[1] is the numeric depth.
    """

    def __init__(self, location: Location, name: str, feature_type: str, depth: int) -> None:
        """
        Initializes a Lake instance.

        Arguments:
            location (Location): The location of the lake.
            name (str): The name of the lake.
            feature_type (str): The type of the feature ("lake").
            depth (int): The depth of the lake.
        """

        # Call the base class constructor
        super().__init__(location, name)

        # Store the feature type and value as a list
        self.feature_type = feature_type
        self.feature_value = ['depth', depth]


    def symbol(self) -> str:
        """
        Returns the symbol for a lake.

        Returns:
            str: 'l'
        """

        # Return 'l' for lake
        return 'l'


class Crater(GeoFeature):
    """
    Crater class for representing crater features.

    Instance Variables:
        feature_type (str): The type of the feature ("crater").
        feature_value (list): A list where feature_value[0] is the string 'perimeter' and feature_value[1] is the numeric perimeter.
    """

    def __init__(self, location: Location, name: str, feature_type: str, perimeter: int) -> None:
        """
        Initializes a Crater instance.

        Arguments:
            location (Location): The location of the crater.
            name (str): The name of the crater.
            feature_type (str): The type of the feature ("crater").
            perimeter (int): The perimeter of the crater.
        """

        # Call the base class constructor
        super().__init__(location, name)

        # Store the feature type and value as a list
        self.feature_type = feature_type
        self.feature_value = ['perimeter', perimeter]


    def symbol(self) -> str:
        """
        Returns the symbol for a crater.

        Returns:
            str: 'c'
        """

        # Return 'c' for crater
        return 'c'