#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See LICENSE.txt included in this distribution for the specific
# language governing permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at LICENSE.txt.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

import logging
import argparse


class LogLevelAction(argparse.Action):
    """
    This class is supposed to be used as action for argparse.
    The action is handled by trying to find the option argument as attribute
    in the logging module. On success, its numeric value is stored in the
    namespace, otherwise ValueError exception is thrown.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(LogLevelAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # print('%r %r %r' % (namespace, values, option_string))
        val = get_log_level(values)
        if val:
            setattr(namespace, self.dest, val)
        else:
            raise ValueError("invalid log level '{}'".format(values))


def get_log_level(level):
    """
    :param level: expressed in string (upper or lower case) or integer
    :return: integer representation of the log level or None
    """
    if type(level) is int:
        return level

    # This could be a string storing a number.
    try:
        return int(level)
    except ValueError:
        pass

    # Look up the name in the logging module.
    try:
        value = getattr(logging, level.upper())
        if type(value) is int:
            return value
        else:
            return None
    except AttributeError:
        return None