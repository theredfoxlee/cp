#!/usr/bin/env python3

import os
import sys


def cp_file(source, destination):
    """Copies the source to destination"""
    with open(source, 'rb') as ifs:
        with open(destination, 'wb') as ofs:
            data_block = 4000
            read_data = ifs.read(data_block)
            while len(read_data) > 0:
                ofs.write(read_data)
                read_data = ifs.read(data_block)


def cp_dir(source, destination):
    """Copies the source directory to the destination directory"""
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    source_parent = os.path.split(source)[0]

    for root, dirs, files in os.walk(source):
        relative_path = root.replace(source_parent + '/', "")
        new_dir_destination = os.path.join(destination, relative_path)
        os.mkdir(new_dir_destination)

        for file in files:
            file_old_location = os.path.join(root, file)
            file_new_location = os.path.join(new_dir_destination, file)

            cp_file(file_old_location, file_new_location)


def get_path_type(sources):
    """Returns path-type dictionary"""
    path_type = {}
    for source in sources:
        if os.path.isfile(source):
            path_type[source] = 'file'
        elif os.path.isdir(source):
            path_type[source] = 'dir'
        else:
            print("The system cannot find {}.".format(source), file=sys.stderr)
            return {}
    return path_type


def main():
    """Manages th cp.py"""
    argc = len(sys.argv)
    if argc <= 2:
        print("The syntax of the command is incorrect.", file=sys.stderr)
    else:
        path_type = get_path_type(sys.argv[1:argc-1])

        for path, type in path_type.items():
            if type == 'file':
                cp_file(path, sys.argv[-1])
            elif type == 'dir':
                cp_dir(path, sys.argv[-1])


if __name__ == '__main__':
    main()