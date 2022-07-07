import csv
from datetime import timedelta

from .abstract import LoaderStep


DATE_FORMAT = "%Y-%m-%d"


class CreateFileForSongsStep(LoaderStep):
    """
    Iterate over the file and put a row for each different song and for
    each different dates despite if not all the dates are contained
    in the input file. Put the count on 0 for each date.

    Complexity O(N^2).
    """

    # Dump into the output_file a max of  MAX_ROW_UPDATE values.
    MAX_ROW_UPDATE = 10**6

    def __init__(self, input_file, output_file, start_date, end_date):
        self.input_file = input_file
        self.output_file = output_file
        self.start_date = start_date
        self.end_date = end_date

    @property
    def prov_file(self) -> str:
        """Returns the provisional file generated with these empty data."""

        return f"{self.output_file}.prov"

    @property
    def date_array(self) -> iter:
        """Returns all the days between the start and end date in an iterable"""

        delta = self.end_date - self.start_date
        for i in range(delta.days + 1):
            yield (self.start_date + timedelta(days=i)).strftime(DATE_FORMAT)

    def _start(self) -> str:
        with open(self.input_file, "r") as input_ftx:
            input_reader = csv.reader(input_ftx, delimiter=",")
            next(input_reader)  # Headers

            first_push = True
            next_song_push = set()
            for input_row in input_reader:
                input_song = input_row[0]
                next_song_push.add(input_song)

                # If max elements are reached, drop them into the file
                if len(next_song_push) > self.MAX_ROW_UPDATE:
                    self.push_input_songs_to_file(next_song_push, first_push=first_push)
                    first_push = False
                    next_song_push = set()

            # Dump the last chunk of songs into the output file
            self.push_input_songs_to_file(next_song_push, first_push=first_push)

        return self.prov_file

    def push_input_songs_to_file(self, next_song_push, first_push=False) -> None:
        """Push songs into the output file. Check which song are in the final
        file, and if they're not, push them onto it."""

        if not first_push:
            next_song_push = self.get_new_songs(next_song_push)
        self.write_new_songs_to_file(next_song_push)

    def get_new_songs(self, songs) -> set:
        """Get the new songs that are not in the output file"""

        new_songs = set()

        with open(self.prov_file, "r") as output_ftx:
            output_reader = csv.reader(output_ftx, delimiter=",")

            # Iterate all the songs that wants to be dropped into
            # the output file
            for song in songs:
                exists = True
                for output_row in output_reader:
                    if song == output_row[0]:
                        exists = False
                        break

                # Song doesn't exist in the file yet. Add it. Restart
                # output_file reading
                output_ftx.seek(0)
                if exists:
                    new_songs.add(song)
        return new_songs

    def write_new_songs_to_file(self, songs) -> None:
        """Write the new songs with all the dates into the file.
        Be careful of that songs. It must not exist into the file,
        otherwise it will be repeated"""

        with open(self.prov_file, "w") as output_ftx:
            writer = csv.writer(output_ftx, delimiter=",")
            for song in songs:
                for date in self.date_array:
                    writer.writerow([song, date])
