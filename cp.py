#!/usr/bin/env python3

""" This module contains cp function. """


__author__ = 'Kamil Janiec <kamil.p.janiec@gmail.com>'


import os


def cp(src, dst, overwrite=False, chunk_size=65536):
    """ Copy file from src to dst. """
    src = os.path.realpath(src)
    dst = os.path.realpath(dst)

    if not os.path.exists(src):
        raise FileNotFoundError(f'No such file: {src}')
    
    if os.path.isdir(src):
        raise IsADirectoryError(f'Is a directory: {src}')

    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    if os.path.isdir(dst):
        raise IsADirectoryError(f'Is a directory: {dst}')

    if os.path.isfile(dst) and overwrite is False:
        raise FileExistsError(f'File exists: {dst}')

    with open(src, 'rb') as src_fh:
        with open(dst, 'wb') as dst_fh:
            for chunk in iter(lambda: src_fh.read(chunk_size), b''):
                dst_fh.write(chunk)


def cp_r(src, dst):
    """ Copy dir from src to dst. """ 
    src = os.path.realpath(src)
    dst = os.path.realpath(dst)

    if not os.path.exists(src):
        raise FileNotFoundError(f'No such directory: {src}')
    
    if os.path.isfile(src):
        raise NotADirectoryError(f'Not a directory: {src}')

    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    if os.path.isfile(dst):
        raise NotADirectoryError('Not a directory: {dst}')

    if os.path.isdir(dst):
        raise FileExistsError(f'Directory exists: {dst}')
    
    if not os.path.isdir(dst):
        os.mkdir(dst)

    for root, dirs, files in os.walk(src):
        for dir_ in dirs:
            dir_ = os.path.join(root, dir_)
            os.mkdir(os.path.join(dst, os.path.relpath(dir_, src)))
        for file_ in files:
            file_ = os.path.join(root, file_)
            cp(file_, os.path.join(dst, os.path.relpath(file_, src)))


if __name__ == '__main__':
    cp_r('distcc-9', 'distcc-99')
