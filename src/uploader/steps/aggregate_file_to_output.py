import csv

from .abstract import LoaderStep


class AggregateFileToOutputStep(LoaderStep):
    """
    Add up the values to the end_file. It won't use any clue about where's the song.
    Just iterate over the input file adding up the values that match song and date.

    Complexity: O(N·logN)
    """

    def __init__(self, input_file, song_empty_file, output_file):
        self.input_file = input_file
        self.song_empty_file = song_empty_file
        self.output_file = output_file

    def _start(self) -> None:
        with open(self.output_file, "w") as output_ftx:
            writer = csv.writer(output_ftx, delimiter=",")

            with open(self.input_file, "r") as input_ftx:
                input_reader = csv.reader(input_ftx, delimiter=",")
                writer.writerow(next(input_reader))

                with open(self.song_empty_file, "r") as song_empty_ftx:
                    song_empty_reader = csv.reader(song_empty_ftx, delimiter=",")

                    # For each song, count how many plays has. Put them
                    # into the final file.
                    for song, date in song_empty_reader:
                        plays = self.count_plays_for_song_and_date(
                            song,
                            date,
                            input_reader,
                        )

                        # If plays are bigger than 0, add them into the final file.
                        # Sorting is ensured because the song_empty_files is iterated
                        # correctly, first by song, and then by date.
                        if plays > 0:
                            writer.writerow([song, date, plays])

                        # Restart input file for allowing searching again on the next
                        # combination of song-date.
                        input_ftx.seek(0)

    def count_plays_for_song_and_date(self, song, date, input_reader) -> int:
        plays = 0
        for song_data in input_reader:
            if song_data[0] == song and song_data[1] == date:
                plays += int(song_data[2])
        return plays
