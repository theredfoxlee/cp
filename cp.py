#!/usr/bin/python3.5

import os
import sys


def cp_file(source, destination, data_block=4096):
    """Copies the source to destination"""

    if os.path.exists(destination):
        print("Copy is not feasible. "
              "File already exists: {}".format(destination), file=sys.stderr)
    else:
        with open(source, 'rb') as ifs:
            with open(destination, 'wb') as ofs:
                read_data = ifs.read(data_block)
                while len(read_data) > 0:
                    ofs.write(read_data)
                    read_data = ifs.read(data_block)


def cp_dir(source, destination):
    """Copies the source directory to the destination directory."""

    source_parent = os.path.dirname(source)

    for root, dirs, files in os.walk(source):
        """Preparation of fixed destination."""
        relative_path = root.replace(source_parent, "")[1:]
        fixed_destination = os.path.join(destination, relative_path)

        if os.path.exists(fixed_destination):
            print("Copy is not feasible. "
                  "File already exists: {}".format(fixed_destination), file=sys.stderr)
        else:
            """Creation of new directory."""
            os.mkdir(fixed_destination)

        for file in files:
            """Preparation of old and new absolute paths."""
            file_old_location = os.path.join(root, file)
            file_new_location = os.path.join(fixed_destination, file)
            """Copying the file."""
            cp_file(file_old_location, file_new_location)


def is_syntax_valid():
    """Syntax pre-check."""

    if len(sys.argv) < 3:
        return False
    else:
        return True


def are_paths_valid(paths):
    """Paths pre-check."""

    for path in paths:
        if not os.path.exists(path):
            return False

    return True


def get_abs_paths(paths):
    """Returns absolute paths sequence"""

    abs_paths = []

    for path in paths:
        abs_paths.append(os.path.abspath(path))

    return abs_paths


def main():

    if not is_syntax_valid():
        print("The syntax of the command is incorrect.", file=sys.stderr)
        return 1
    elif not are_paths_valid(sys.argv[1:]):
        print("Some paths are not valid", file=sys.stderr)
        return 2

    abs_paths = get_abs_paths(sys.argv[1:-1])
    destination = os.path.abspath(sys.argv[-1])

    for file in abs_paths:
        if os.path.isdir(file):
            cp_dir(file, destination)
        elif os.path.isfile(file):
            file_name = os.path.basename(file)
            fixed_destination = os.path.join(destination, file_name)
            cp_file(file, fixed_destination)
        else:
            print("Unknown file will not be copied: "
                  "{}".format(file))

    return 0


if __name__ == '__main__':
    main()
