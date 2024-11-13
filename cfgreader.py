import argparse
import base64
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="MEGASync Configfile parser",
        description="Decodes values in CFG file",
    )
    parser.add_argument("input_file", help="MEGASync.cfg file.")
    parser.add_argument("output_file", help="Filename to write results to.")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwriting output file if it exists.",
    )
    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_file = Path(args.output_file)

    if output_file.exists() and not args.force:
        print(
            "Output file already exists. Please (re)move the file or use -f to force overwriting."
        )
        exit(1)

    with open(input_file, "r") as infile:
        with open(output_file, "w") as outfile:
            for inline in infile.readlines():
                if inline[0] == "[" or inline == "\n":
                    outfile.write(inline)
                    continue
                identifier, base64blob = inline.split("=", 1)
                stripped_base64 = base64blob.strip("\n").strip('"')
                outfile.write(
                    f"{identifier}={base64.b64decode(stripped_base64).decode()}\n"
                )


if __name__ == "__main__":
    main()
