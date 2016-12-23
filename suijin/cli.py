"""cli: interpret command line arguments given.

This module wraps the `argparse` module from Python's standard library to read
arguments provided when invoking this tool. Only two positional arguments are
supported:

    `input`  - the path to a TIF file containing elevation data
    `output` - the path where the output of this program will be stored, in TIF format
"""

import argparse

def run():
    parser = _build_parser()
    _add_arguments(parser)

    return parser.parse_args()

def _build_parser():
    return argparse.ArgumentParser(
        prog='suijin',
        description='Calculates flow direction and accumulation for given elevation data.',
        epilog='Renato M. Costa - MIT License'
    )

def _add_arguments(parser):
    parser.add_argument('input',
        metavar='input',
        type=str,
        help='the path to a TIF file containing the elevation data'
    )

    parser.add_argument('output',
        metavar='output',
        type=str,
        help='path to the file where the output (in TIF format) will be stored'
    )
