#!/usr/bin/python3

import argparse
import sys
import unittest

sys.path.append("Other/")

from xstrategy import xstrategy
from xstrategy_tests import XStrategyTests


if __name__ == "__main__":
    # Add optional argument to enable unit testing
    parser = argparse.ArgumentParser(description="Run xstrategy or unit tests")
    parser.add_argument("-u", "--unit", help="Run unit tests", action="store_true")

    args = vars(parser.parse_args())

    # Reset the command line arguments to prevent "unit" argument from being
    # passed to xstrategy
    sys.argv = ["xstrategy"]

    # If unit argument was provided, run the unit tests. Otherwise, call xstrategy
    if args['unit']:
        unittest.main()
    else:
        xstrategy()
