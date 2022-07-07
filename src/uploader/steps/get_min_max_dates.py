import csv
import datetime

from .abstract import LoaderStep


DATE_FORMAT = "%Y-%m-%d"


class GetMinMaxDateStep(LoaderStep):
    """
    Get the oldest and newest dates of the file from 1st iteration.
    Return datetime objects with these two dates.

    Complexity order: O(N)
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def _start(self):
        with open(self.file_path, "r") as ftx:
            reader = csv.reader(ftx, delimiter=",")

            next(reader)  # Headers
            first_row = next(reader)
            min_date = max_date = datetime.datetime.strptime(first_row[1], DATE_FORMAT)

            for row in reader:
                date = datetime.datetime.strptime(row[1], DATE_FORMAT)
                if date < min_date:
                    min_date = date
                elif date > max_date:
                    max_date = date

        return min_date, max_date
