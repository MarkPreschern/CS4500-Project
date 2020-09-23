#!/usr/bin/python3

import sys
import json


def is_math_symbol(s):
    """
    Checks if the provided string is either a number
    or any other valid character in a JSON number.

    :param s: string to check
    :return: boolean indicating whether the statement
             above holds true
    """
    lst = [str(chr) for chr in list(range(0, 10))]
    lst.extend(['.', 'e', '+', '-', 'E'])
    return s in lst


def get_json_vals(str):
    """
    Returns all JSON values from string sequence.

    :param str: string of JSON values
    """
    # Initialize start cursor
    start_index = 0

    # Initialize array to hold matched JSON values
    objects = []

    # Initialize flags to keep track of
    # whether we've seen e and/or . in the
    # current substring.
    seen_e = False
    seen_period = False

    # Scan down string and extract JSON values
    for k in range(1, len(str)):
        # print('looking at {}'.format(str[start_index:k + 1]))
        # Check to see if current character is a digit and
        # is followed by digits, . or e

        # Checking to see if we've parsed the whole number
        if is_math_symbol(str[k]) and k < len(str) - 1 and is_math_symbol(str[k + 1]):
            # Set flags for e and . if match occurs
            if str[k] == '.':
                seen_period = True
            elif str[k].lower() == 'e':
                seen_e = True

            # Check if the next character is part of the next number
            if k < len(str) - 2 and is_math_symbol(str[k + 2]):
                # If the (k+2)th character is either . or e then
                # the character the precedes it is part of the next number
                # and we try to parse str[start_index:k+1]
                if (seen_period or seen_e) and str[k + 2] == '.':
                    pass
                elif seen_e and str[k + 2].lower() == 'e':
                    pass
                else:
                    # We have more digits / characters coming up that
                    # are apart of the current number, so continue.
                    continue
            else:
                continue

        # Attempt to parse current string delimited by
        # start_index and k.
        obj = try_parse_json(str[start_index:k + 1])

        # If the object was parsed successfully as JSON, then append
        # to return []
        if obj is not None:
            # Increment start cursor
            start_index = k + 1
            # Reset flags for e and period
            seen_e = False
            seen_period = False
            # Push JSON value to array
            objects.append(obj)

    # Return matched JSON values
    return objects


def try_parse_json(str):
    """
    Tries to parse given string into JSON object.

    :param str: string to parse
    :return: resulting JSON object if successful and None otherwise
    """
    try:
        return json.loads(str)
    except ValueError:
        return None


objects = []

if __name__ == "__main__":
    # Read lines from STDIN indefinitely until
    # stream is closed
    for k in sys.stdin:
        objects += get_json_vals(k)

    # Make up the objects
    obj1 = {"count": len(objects), "seq": objects}
    obj2 = [len(objects)]
    obj2.extend(objects[::-1])

    # Print the two objects
    print(json.dumps(obj1), json.dumps(obj2))
