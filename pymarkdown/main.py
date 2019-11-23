"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import os
import sys


class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    def __init__(self):
        self.version_number = "0.1.0"

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Lint any found Markdown files.")

        parser.add_argument(
            "--version", action="version", version="%(prog)s " + self.version_number
        )

        parser.add_argument(
            "-l",
            "--list-files",
            dest="list_files",
            action="store_true",
            default=False,
            help="list the markdown files found and exit.",
        )
        parser.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            help="One or more paths to scan for eligible files",
        )
        return parser.parse_args()

    @classmethod
    def is_file_eligible_to_scan(cls, path_to_test):
        """
        Determine if the presented path is one that we want to scan.
        """
        return path_to_test.endswith(".md")

    @classmethod
    def __determine_files_to_scan(cls, eligible_paths):

        files_to_parse = set()
        for next_path in eligible_paths:

            if not os.path.exists(next_path):
                print(
                    "Provided path '" + next_path + "' does not exist. Skipping.",
                    file=sys.stderr,
                )
                continue
            if os.path.isdir(next_path):
                for root, _, files in os.walk(next_path):
                    for file in files:
                        rooted_file_path = os.path.join(root, file)
                        if cls.is_file_eligible_to_scan(rooted_file_path):
                            files_to_parse.add(rooted_file_path)
            else:
                if cls.is_file_eligible_to_scan(next_path):
                    files_to_parse.add(next_path)
                else:
                    print(
                        "Provided file path '"
                        + next_path
                        + "' is not a valid markdown file. Skipping.",
                        file=sys.stderr,
                    )
        files_to_parse = list(files_to_parse)
        files_to_parse.sort()
        return files_to_parse

    @classmethod
    def __handle_list_files(cls, files_to_scan):

        if files_to_scan:
            print("\n".join(files_to_scan))
            return 0
        print("No Markdown files found.", file=sys.stderr)
        return 1

    def main(self):
        """
        Main entrance point.
        """
        args = self.__parse_arguments()

        files_to_scan = self.__determine_files_to_scan(args.paths)
        if args.list_files:
            return_code = self.__handle_list_files(files_to_scan)
            sys.exit(return_code)


if __name__ == "__main__":
    PyMarkdownLint().main()
