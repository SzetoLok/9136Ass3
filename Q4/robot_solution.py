class Robot:
    """
    Robot class for representing and manipulating robots.

    Instance Variables:
        name (str): The name of the robot.
        phrase (str): The phrase of the robot.

    Class Attributes:
        phrase (str): The default phrase of a robot.
    """

    phrase = "Hello World!" # Class Variable.

    def __init__(self, name): # Constructor (with parameters).
        """ 
        Create a new robot.

        Arguments:
            name (str): The name of the robot.
        """

        self.name = name
        self.phrase = Robot.phrase

    # Methods
    def get_name(self):
        """ 
        Returns the name of the robot.

        Returns:
            str: The name of the robot.
        """

        return self.name

    def get_phrase(self):
        """ 
        Returns the phrase of the robot.

        Returns:
            str: The phrase of the robot.
        """

        return self.phrase

    def set_phrase(self, phrase):
        """ 
        Sets the phrase of the robot.

        Arguments:
            phrase (str): The phrase of the post.
        """

        self.phrase = phrase

    def greet_another_by_name(self, other):
        """ 
        Greets another robot.

        Arguments:
            other (object): The other robot.

        Returns:
            str: The greetings message for the other robot.
        """

        return f"Greetings {other.get_name()}, my name is {self.get_name()}."

    def self_replicate(self):
        """ 
        Self replicates the robot.

        Returns:
            object: New robot with the name Jr. plus the name of the original robot.
        """
        
        return Robot(f"{self.get_name()} Jr.")

class Vacuum(Robot):
    """
    Vacuum class that extends the Robot class for representing and manipulating vacuum cleaners.

    Instance Variables:
        name (str): The name of the vacuum cleaner.
        phrase (str): The phrase of the vacuum cleaner.

    Class Attributes:
        phrase (str): The default phrase of a vacuum cleaner.
    """

    phrase = "Clean World!"

    def __init__(self, name) -> None:
        """ 
        Create a new vacuum cleaner.

        Arguments:
            name (str): The name of the vacuum cleaner.
        """

        super().__init__(name) # Calls the parent class's constructor. We could have also used Robot.__init__(self, name)
        self.phrase = Vacuum.phrase

    def greet_another_by_name(self, robot: object) -> str: # Overrides the parent method.
        """ 
        Greets another robot by overriding the parent's method.

        Arguments:
            other (object): The other robot.

        Returns:
            str: The greetings message for the other robot.
        """

        return super().greet_another_by_name(robot)[:-1] + " and I like to clean." # Invokes the parent method.

    def self_replicate(self) -> object: # Overrides the parent method.
        """ 
        Self replicates the vacuum cleaner by overriding the parent's method.

        Returns:
            object: New vacuum cleaner with the name Jr. plus the name of the original robot.
        """

        return Vacuum(self.get_name() + " Jr.")
