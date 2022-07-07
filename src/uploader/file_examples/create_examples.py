import datetime
import csv
import random


def generate_example_file(n):
    """
    Generates a random file for testing purposes. `n` is the number of
    song records of the input file.
    """

    with open(f"data_{n}_rows.csv", "w") as ftx:
        wr = csv.writer(ftx, delimiter=",")
        wr.writerow(["Song", "Date", "Number of Plays"])

        songs = ["Umbrella", "In the End", "Diamonds", "Rude Boy"]
        today = datetime.date.today()
        dates = [
            (today + datetime.timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range(200)
        ]

        for _ in range(n):
            row = [random.choice(songs), random.choice(dates), random.randint(0, 200)]
            wr.writerow(row)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", dest="rows")
    args = parser.parse_args()

    generate_example_file(int(args.rows))
