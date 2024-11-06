import argparse
from pathlib import Path
from typing import List
import gzip


def parse_filename_from_line(line: str) -> str | None:
    if "transfer->name" not in line:
        return

    log_elements = [element.strip("[]") for element in line.split(" ")]
    timestamp = log_elements[0]
    for index, element in enumerate(log_elements):
        if element == "transfer->name":
            return f"{timestamp}: {log_elements[index+2]}"


def sort_directory_listing(dir_list: List[Path]) -> List[Path]:
    dir_list.sort()  # Sort in place to sort 0 - 9 (zipped) items
    dir_list.insert(0, dir_list.pop())  # Move MEGAsync.log (unzipped) file to the front
    dir_list.reverse()  # Now reverse to order old -> new
    return dir_list


def is_gzipped(filename: Path) -> bool:
    with open(filename, "rb") as testfile:
        first_three_bytes = testfile.read(3)
        return first_three_bytes == b"\x1f\x8b\x08"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="MEGASync Logfile parser",
        description="Filters filenames found in transferlogs",
    )
    parser.add_argument(
        "input_folder", help="Folder where (unzipped) logfiles are to be found."
    )
    parser.add_argument("output_file", help="Filename to write results to.")
    args = parser.parse_args()

    input_folder = Path(args.input_folder)
    if not input_folder.is_dir() or len(list(input_folder.glob("*"))) == 0:
        print("Input folder is not a folder, or is empty. Exiting.")
        exit(1)

    dir_list = [logfile for logfile in input_folder.glob("*") if logfile.is_file()]

    for logfile in dir_list:
        split_name = logfile.name.split(".")
        if "MEGAsync" not in split_name or "log" not in split_name:
            print(f"Input folder seems to contain something else: {logfile.name}")
            exit(1)

    for logfile in sort_directory_listing(dir_list):
        if is_gzipped(logfile):
            infile = gzip.open(logfile, "rt")
        else:
            infile = open(logfile, "r")

        with open(args.output_file, "a") as outfile:
            for line in infile.readlines():
                parsed_line = parse_filename_from_line(line)
                if parsed_line is not None:
                    outfile.write(parsed_line + "\n")
        infile.close()


if __name__ == "__main__":
    main()
