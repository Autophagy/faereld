# -*- coding: utf-8 -*-

"""
faereld.utils
-----------

Various useful static functions and variables for use within Færeld.
"""

from math import floor
from shutil import get_terminal_size
from datetime import datetime
from string import Formatter
from .printer import Printer
import re

header = "FÆRELD :: {0} MODE"

def time_diff(from_date, to_date):
    diff_delta = to_date - from_date
    return format_time_delta(diff_delta)

def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes = floor(remainder/60)

    return "{0}h{1}m".format(floor(hours), minutes)

def print_rendered_string(area_code, area, date_to_display, object_name, duration):

    fields = {
        'area': area_code,
        'area_name': area['name'],
        'object': object_name,
        'date': date_to_display,
        'duration': duration
    }

    printer = Printer()
    for literal, field, _, _ in Formatter().parse(area['rendering_string']):
        if len(literal) > 0:
            printer.add(literal)
        if field is not None:
            if field not in fields:
                raise ValueError("{0} is an invalid rendering string. ".format(area['rendering_string']) +
                                 "Reason: '{1}' is an invalid field.".format(field))
            printer.add_highlighted(fields[field])
    printer.print()

def highlight(item):
    return "\033[94m{0}\033[0m".format(item)

def print_header(string):
    print("\033[91m{0} {1}\033[0m".format(string.upper(), "─"*(terminal_width() - len(string) - 1)))

def terminal_width():
    return get_terminal_size().columns

def max_width(max_config_width):
    return min(terminal_width(), max_config_width)

def strip_colour_codes(string):
    return re.sub('\x1b\[[0-9;]*m', '', string)

def print_areas_help(areas):
    for area_code, area in areas.items():
        print('{0} :: {1}'.format(area_code, area['name']))

def print_projects_help(projects):
    for project_code, project in projects.items():
        print('{0} :: {1} [{2}]'.format(project_code, project['name'], project['link']))
