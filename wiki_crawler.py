import argparse
import subprocess
import time

from validate_directory import ValidateDirectory
from validate_file import ValidateFile


processes = []


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    with open(args.input) as file:
        next(file)
        for _ in range(args.offset):
            next(file)
            
        page_titles = []
        counter = args.offset // args.chunk_size
        for index, line in enumerate(file, start=args.offset):
            page_titles.append(_extract_page_name(line))

            if index % (args.chunk_size - 1) == 0:
                _download_pages(page_titles, f"{args.target}{counter}", args.clients)
                page_titles.clear()
                counter += 1

                if counter >= 10:
                    break

    while len(processes) > 0:
        if not _is_alive(processes[0]):
            processes.pop(0)
        time.sleep(0.05)


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input file, which contains the page information", action=ValidateFile)
    parser.add_argument("--target", required=True, help="the output directory", action=ValidateDirectory)
    parser.add_argument("--chunk-size", required=False, help="the chunk size for downloading pages", default=10, type=int)
    parser.add_argument("--clients", required=False, help="the maximum number of clients to spawn", default=32, type=int)
    parser.add_argument("--offset", required=False, help="the offset (first page) to start with", default=0, type=int)
    return parser


def _extract_page_name(line):
    return line.split(",")[1].replace("\"", "")


def _download_pages(titles, file_name, max_clients):
    while len(processes) >= max_clients:
        for process in processes:
            if not _is_alive(process):
                processes.remove(process)
                break

        time.sleep(0.05)

    process = subprocess.Popen(["curl", "-s", "-d", f"\"&action=submit&pages={'%0A'.join(titles)}\"",
                    "https://en.wikipedia.org/w/index.php?title=Special:Export", "-o", file_name, ">", "/dev/null"],
                               shell=False, stdin=None, stdout=None, stderr=None)
    processes.append(process)


def _is_alive(process):
    if not process:
        return False

    return process.poll() is None


if __name__ == "__main__":
    main()
