import traceback
import logging
import time

from .loaders.brute_force import BruteForceLoader


def process_file(input_file, output_file):
    """
    Main function of this module is `process_file`. Basically transforms
    an input_file into a summarized sorted file. Returns a boolean weather
    the process has finished correctly or not.
    """

    ti = time.time()
    logging.info(f"PROCESSING STARTED")
    loader = BruteForceLoader(input_file, output_file)

    # Start processing the file synchronously
    try:
        loader.start()
    except Exception as e:
        logging.critical(
            f"LOADING ERROR OF FILE: {input_file}. Reason: {traceback.format_exc()}"
        )
        return False, e

    logging.info(f"PROCESSING FINISHED. Took: {(time.time()-ti)/60} seconds.")
    return True, None
