import functools
import os
import re
from cloudconvert.cloudconvertrestclient import default_client

from utils import _combine_dict

valid_conversions = None


def _get_valid_conversions():
    """GET supported conversion formats from CloudConvert
    """
    global valid_conversions
    if valid_conversions:
        return valid_conversions
    res = default_client().get(action='v2/convert/formats')
    valid_conversions = functools.reduce(
        _combine_dict('input_format', 'output_format'),
        res['data'],
        dict())
    return valid_conversions


def _validate_dir(directory: str):
    """Ensure given directory exists.

    We only create subdirectories, so the main directory should be present.
    """
    if not os.path.isdir(directory):
        raise ValueError(f'{directory} is not a directory')


def _validate_conversion(source: str, dest: str):
    """Ensure given combination is a valid conversion supported by CloudConvert
    """
    conversions = _get_valid_conversions()
    if source not in conversions or dest not in conversions[source]:
        raise ValueError(f'Unsupported conversion from {source} to {dest}')


def _validate_conversions(conversions):
    """Ensure given combinations are a valid conversion supported by CloudConvert
    and each input format given is unique.
    """
    seen = set()
    for c in conversions:
        if c[0] in seen:
            raise ValueError(f'Duplicate input format detected: {c[0]}')
        _validate_conversion(c[0], c[1])
        seen.add(c[0])


def validate_args(args):
    _validate_dir(args.src)
    _validate_dir(args.dest)
    if args.conversions:
        _validate_conversions(args.conversions)
