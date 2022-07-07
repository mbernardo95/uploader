import os
import csv
from unittest import TestCase

from ..loaders.brute_force import BruteForceLoader


def run_loader_for_testing(rows):
    # Create a provisional song file with the rows
    provisional_file = "test_simple_composition.csv"
    with open(provisional_file, "w") as ftx:
        writer = csv.writer(ftx, delimiter=",")
        writer.writerow(["Song", "Date", "Number of plays"])
        for row in rows:
            writer.writerow(row)
    provisional_output_file = "output_test_simple_composition.csv"

    # Execute the loader
    loader = BruteForceLoader(
        input_file=provisional_file,
        output_file=provisional_output_file,
    )
    loader.start()

    # Read the output file and delete it. Don't use it with
    # very large files.
    with open(provisional_output_file, "r") as ftx:
        final_rows = [r for r in csv.reader(ftx, delimiter=",")]
    os.remove(provisional_output_file)
    os.remove(provisional_file)

    # Don't return the header, for testing purposes
    return final_rows[1:]


class LoaderTest(TestCase):
    def test_single_song(self):
        rows = [["Song1", "2022-01-15", "10"]]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 1)
        self.assertEqual(["Song1", "2022-01-15", "10"], rows[0])

    def test_single_song_aggregation(self):
        rows = [
            ["Song1", "2022-01-16", "10"],
            ["Song1", "2022-01-16", "20"],
        ]
        rows = run_loader_for_testing(rows)
        self.assertEqual(len(rows), 1)
        self.assertIn(["Song1", "2022-01-16", "30"], rows)

    def test_multiple_songs(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song2", "2022-01-16", "20"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "10"], rows)
        self.assertIn(["Song2", "2022-01-16", "20"], rows)

    def test_multiple_songs_aggregation(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song2", "2022-01-16", "20"],
            ["Song1", "2022-01-15", "5"],
            ["Song2", "2022-01-16", "6"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "15"], rows)
        self.assertIn(["Song2", "2022-01-16", "26"], rows)

    def test_multiple_dates_without_holes(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-01-16", "20"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "10"], rows)
        self.assertIn(["Song1", "2022-01-16", "20"], rows)

    def test_multiple_dates_without_holes_aggregation(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-01-16", "20"],
            ["Song1", "2022-01-15", "5"],
            ["Song1", "2022-01-16", "6"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "15"], rows)
        self.assertIn(["Song1", "2022-01-16", "26"], rows)

    def test_multiple_dates_with_holes(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-02-17", "20"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "10"], rows)
        self.assertIn(["Song1", "2022-02-17", "20"], rows)

    def test_multiple_dates_with_holes_aggregation(self):
        rows = [
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-02-17", "20"],
            ["Song1", "2022-01-15", "5"],
            ["Song1", "2022-02-17", "6"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "15"], rows)
        self.assertIn(["Song1", "2022-02-17", "26"], rows)

    def test_multiple_dates_unsorted(self):
        rows = [
            ["Song1", "2022-02-17", "20"],
            ["Song1", "2022-01-15", "10"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "10"], rows)
        self.assertIn(["Song1", "2022-02-17", "20"], rows)

    def test_multiple_dates_unsorted_aggregation(self):
        rows = [
            ["Song1", "2022-02-17", "20"],
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-02-17", "5"],
            ["Song1", "2022-01-15", "6"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 2)
        self.assertIn(["Song1", "2022-01-15", "16"], rows)
        self.assertIn(["Song1", "2022-02-17", "25"], rows)

    def test_date_sorting(self):
        rows = [
            ["Song1", "2022-02-17", "20"],
            ["Song1", "2022-01-15", "10"],
            ["Song1", "2022-03-17", "5"],
            ["Song1", "2022-01-14", "6"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 4)
        self.assertIn(["Song1", "2022-01-14", "6"], rows)
        self.assertIn(["Song1", "2022-01-15", "10"], rows)
        self.assertIn(["Song1", "2022-02-17", "20"], rows)
        self.assertIn(["Song1", "2022-03-17", "5"], rows)
        self.assertEqual(rows.index(["Song1", "2022-01-14", "6"]), 0)
        self.assertEqual(rows.index(["Song1", "2022-01-15", "10"]), 1)
        self.assertEqual(rows.index(["Song1", "2022-02-17", "20"]), 2)
        self.assertEqual(rows.index(["Song1", "2022-03-17", "5"]), 3)

    def test_complete(self):
        rows = [
            ["Song1", "2022-01-15", "1"],
            ["Song2", "2022-01-13", "10"],
            ["Song1", "2022-02-15", "100"],
            ["Song3", "2022-03-15", "1000"],
            ["Song2", "2022-01-13", "10000"],
        ]
        rows = run_loader_for_testing(rows)

        self.assertEqual(len(rows), 4)
        self.assertIn(["Song1", "2022-01-15", "1"], rows)
        self.assertIn(["Song1", "2022-02-15", "100"], rows)
        self.assertIn(["Song2", "2022-01-13", "10010"], rows)
        self.assertIn(["Song3", "2022-03-15", "1000"], rows)
        self.assertEqual(
            rows.index(["Song1", "2022-01-15", "1"]) + 1,
            rows.index(["Song1", "2022-02-15", "100"]),
        )
