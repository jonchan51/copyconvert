import argparse
import cloudconvert
from dotenv import load_dotenv
import logging
import multiprocessing.dummy as mp
import os
from shutil import copyfile
import sys

from convert import convert
from validate import validate_args


def main(src, dest, conversions, skips):
    success = []
    fail = []

    def copyconvert(line):
        fp = line.strip()
        # skip current file if filepath matches any of the given regex
        skip = True in [s in fp for s in skips]

        if not skip:
            logging.debug(f'Attempting to transfer {fp}')
            ori_fp = fp
            name, ext = os.path.splitext(fp)
            ori_ext = ext

            if ori_ext[1:] in conversions:
                ext = '.' + conversions[ori_ext[1:]]

            rel_path = os.path.relpath(name + ext, src)
            abs_path = os.path.join(dest, rel_path)

            # skip file if it exists in destination folder
            if os.path.exists(abs_path):
                print(f'{abs_path} already exists!')
                return

            if ori_ext[1:] in conversions:
                print(f'Converting {fp} to {ext[1:]}')
                fp = convert(fp, ext[1:])
                print(f'Converted {fp} to {ext[1:]}')

            # create folders if they dont exist
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            # copy file
            copyfile(fp, abs_path)
            logging.debug(f'Transferred {ori_fp} to {abs_path}')
            success.append(abs_path)

    lines = sys.stdin.readlines()

    # Multithread
    p = mp.Pool(10)
    p.map(copyconvert, lines)
    p.close()
    p.join()

    # dump failed conversions to stderr log and a file
    if len(fail) > 0:
        pass

    if len(success) == 0:
        print('No files were transferred.')
    else:
        print(f'Finished transferring all files to {dest}')
        print('==============================================')
        print('             Transferred files                ')
        print('==============================================')
        # list all files transferred
        success.sort()
        # Can consider pretty printing
        for fp in success:
            print(fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Transfer a list of files, passed in via stdin, to some \
            destination folder, with optional file conversions via CloudConvert')
    parser.add_argument('-s', '--src',
                        required=True,
                        help='Source folder',
                        dest='src',
                        metavar='source')
    parser.add_argument('-d', '--dest',
                        required=True,
                        help='Destination folder',
                        dest='dest',
                        metavar='destination')
    parser.add_argument('-c', '--convert',
                        help='Converts files <from> type to <to> type',
                        metavar=('from', 'to'),
                        dest='conversions',
                        action='append',
                        nargs=2)
    parser.add_argument('--skip',
                        help='Skips if filename includes provided string',
                        metavar='string',
                        dest='skips',
                        action='append')
    parser.add_argument('-l', '--log',
                        help='Indicate logging level',
                        default='ERROR',
                        dest='loglevel',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel))

    load_dotenv()
    cloudconvert.configure(api_key=os.getenv('CLOUDCONVERT_API_KEY'))

    validate_args(args)

    conversions = dict()
    if args.conversions:
        for c in args.conversions:
            conversions[c[0]] = c[1]

    main(args.src, args.dest, conversions, args.skips)
