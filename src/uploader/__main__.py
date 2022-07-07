if __name__ == "__main__":
    import argparse
    from . process import process_file

    parser = argparse.ArgumentParser(description="Processing music files! :)")
    parser.add_argument("--input-file", dest="input_file")
    parser.add_argument("--output-file", dest="output_file")
    args = parser.parse_args()

    process_file(args.input_file, args.output_file)
