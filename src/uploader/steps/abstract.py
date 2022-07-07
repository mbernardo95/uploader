import abc
import time
import logging


class LoaderStep(abc.ABC):
    def start(self):
        """Public method for starting the step."""

        ti = time.time()
        logging.info("Starting step: ", self.__class__.__name__)
        result = self._start()
        eta = time.time() - ti
        logging.info(f"Finished step: {self.__class__.__name__} in {eta} seconds")
        return result

    @abc.abstractmethod
    def _start(self):
        """Override this method on different steps in order to make the
        corresponding actions."""
        pass
