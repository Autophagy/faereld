# -*- coding: utf-8 -*-

"""
faereld.controller
------------------

"""

from .db import FaereldData
from . import utils

from os import path
import datarum
import datetime

class Controller(object):

    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.db = FaereldData(self.data_path)

    # Summary Mode

    def summary(self):
        summary = self.db.get_summary(detailed=True)

        print()
        print(utils.header.format("SUMMARY"))
        summary.print()

    # Insert Mode

    def insert(self):
        summary = self.db.get_summary()

        print()
        print(utils.header.format("INSERT"))
        summary.print()

        print()
        print("[ Areas :: {0} ]".format(' // '.join(utils.areas.keys())))
        area = input('Area :: ').upper()

        if area in utils.project_areas:
            object, link = self._project_object()
        else:
            object, link = self._non_project_object()

        # Assume to be in the form [date // time]
        print()
        from_date = input('From :: ')
        wending_date, from_date_gregorian = self.convert_input_date(from_date)

        to_date = input('To :: ')
        _, to_date_gregorian = self.convert_input_date(to_date)

        time_diff = self._time_diff(from_date_gregorian, to_date_gregorian)

        print()
        if area in utils.project_areas:
            print(utils.rendering_strings['projects'].format(wending_date.formatted(),
                                                       object,
                                                       utils.areas[area],
                                                       time_diff))
        else:
            print(utils.rendering_strings[area].format(wending_date.formatted(),
                                                 object,
                                                 time_diff))

        confirmation = input("Is this correct? (y/n) :: ")

        if confirmation.lower() == 'y':
            self.db.create_entry(area,
                                 object,
                                 link,
                                 from_date_gregorian,
                                 to_date_gregorian)

            print("Færeld entry added")
        else:
            print("Færeld entry cancelled")

    def _project_object(self):
        projects = self.config.get_projects()

        print()
        print("[ Objects :: {0} ]".format(' // '.join(projects.keys())))
        object = input('Object :: ')

        while object not in projects:
            print()
            print("Invalid Project :: {0}".format(object))
            object = input('Object :: ')

        object_name = projects[object]['name']
        link = projects[object]['link']

        return (object_name, link)

    def _non_project_object(self):
        object = input('Object :: ')

        return (object, None)

    def convert_input_date(self, date_string):
        date, time = date_string.split(' // ')
        wending_date = datarum.wending.from_date_string(date)
        gregorian_date = datarum.to_gregorian(wending_date)
        time = datetime.datetime.strptime(time, '%H.%M')

        return (wending_date,
                gregorian_date.replace(hour=time.hour, minute=time.minute))

    def _time_diff(self, from_date, to_date):
        diff_delta = to_date - from_date
        return utils.format_time_delta(diff_delta)

    # Sync Mode

    def sync(self):

        print()
        print(utils.header.format("SYNC"))
        print("Sync mode is currently not enabled.")
