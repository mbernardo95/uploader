import abc


class IFileLoader(abc.ABC):
    """
    Every FileLoader method has to inherit from this base class.
    Acts as an interface.
    """

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    @abc.abstractmethod
    def start(self):
        """Start is the main function of the method. Executes
        the loader main method for creating the end_file."""
