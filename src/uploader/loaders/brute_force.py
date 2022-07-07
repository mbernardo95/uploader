import os

from .abstract import IFileLoader

from ..steps import (
    GetMinMaxDateStep,
    CreateFileForSongsStep,
    AggregateFileToOutputStep,
)


class BruteForceLoader(IFileLoader):
    """
    Brute Force method. Steps:
    1. Get the oldest and newest dates of the file from 1st iteration. O(N)
    2. Iterate over the file and put a row for each different song and for
       each different dates despite if not all the dates are contained
       in the input file. O(N^2)
    3. Start a new iteration adding up the values to the end_file. It won't
       use any clue about where's the song. Just iterate over the file until
       finding it. O(N·log(N))
    4. Delete the provisional file generated at #3.

    Complexity summary: O(N^2)
    """

    def start(self):
        # Step 1: Get oldest and newest dates
        step1 = GetMinMaxDateStep(file_path=self.input_file)
        min_date, max_date = step1.start()

        # Step 2: Build output_file empty
        step2 = CreateFileForSongsStep(
            input_file=self.input_file,
            output_file=self.output_file,
            start_date=min_date,
            end_date=max_date,
        )
        prov_output_file = step2.start()

        # Step 3: Aggregate the values
        step3 = AggregateFileToOutputStep(
            input_file=self.input_file,
            song_empty_file=prov_output_file,
            output_file=self.output_file,
        )
        step3.start()

        # Step 4: Delete provisional file
        os.remove(prov_output_file)
