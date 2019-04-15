import argparse
import subprocess

from validate_directory import ValidateDirectory
from validate_file import ValidateFile


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    with open(args.input) as file:
        next(file)
        page_titles = []
        counter = 0
        for index, line in enumerate(file, start=1):
            page_titles.append(_extract_page_name(line))

            if index % args.chunk_size == 0:
                _download_pages(page_titles, f"{args.target}{counter}")
                page_titles.clear()
                counter += 1
                
                if counter >= 10:
                    return


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input file, which contains the page information", action=ValidateFile)
    parser.add_argument("--target", required=True, help="the output directory", action=ValidateDirectory)
    parser.add_argument("--chunk-size", required=False, help="the chunk size for downloading pages", default=10, type=int)
    return parser


def _extract_page_name(line):
    return line.split(",")[1].replace("\"", "")


def _download_pages(titles, file_name):
    subprocess.run(["curl", "-d", f"\"&action=submit&pages={'%0A'.join(titles)}\"",
                    "https://en.wikipedia.org/w/index.php?title=Special:Export", "-o", file_name])


if __name__ == "__main__":
    main()