from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Location:
    Y: int = 0
    X: int = 0

    def __str__(self):
        return f"({self.Y},{self.X})"

@dataclass
class Size:
    height: int = 0
    width: int = 0


class GeoFeature(ABC):
    def __init__(self, location, name):
        self.location = location
        self.name = name

    @abstractmethod
    def symbol(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Mountain(GeoFeature):

    def __init__(self, location, name, height):
        super().__init__(location, name)
        self.height = height

    def symbol(self):
        return 'm'

    def __str__(self):
        return f"mountain {self.name}, height {self.height}"


class Lake(GeoFeature):

    def __init__(self, location, name, depth):
        super().__init__(location, name)
        self.depth = depth

    def symbol(self):
        return 'l'

    def __str__(self):
        return f"lake {self.name}, depth {self.depth}"

class Crater(GeoFeature):

    def __init__(self, location, name, perimeter):
        super().__init__(location, name)
        self.perimeter = perimeter

    def symbol(self):
        return 'c'

    def __str__(self):
        return f"crater {self.name}, perimeter {self.perimeter}"