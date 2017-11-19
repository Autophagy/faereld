# -*- coding: utf-8 -*-

"""
faereld.controller
------------------

"""

from . import models
from os import path
import sqlalchemy
import datarum
import datetime
import math

class Controller(object):

    project_areas = {
        'RES': 'Research',
        'DES': 'Design',
        'DEV': 'Development',
        'DOC': 'Documentation',
        'TST': 'Testing',
    }

    misc_areas = {
        'IRL': 'Real life engagements (confs/talks/meetups)',
        'RDG': 'Reading',
        'LNG': 'Languages',
        'BKG': 'Baking'
    }

    areas = project_areas.copy()
    areas.update(misc_areas)

    rendering_strings = {
        'projects': 'On \033[94m{0}\033[0m I worked on \033[94m{1}\033[0m (\033[94m{2}\033[0m) for \033[94m{3}\033[0m',
        'IRL': 'On \033[94m{0}\033[0m I was at \033[94m{1}\033[0m for \033[94m{2}\033[0m',
        'RDG': 'On \033[94m{0}\033[0m I read \033[94m{1}\033[0m for \033[94m{2}\033[0m',
        'LNG': 'On \033[94m{0}\033[0m I learned \033[94m{1}\033[0m for \033[94m{2}\033[0m',
        'BKG': 'On \033[94m{0}\033[0m I made \033[94m{1}\033[0m for \033[94m{2}\033[0m'
    }


    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.session = self.create_session(self.data_path)

    # [ Filesystem Reading / Writing ]

    def create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        models.FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()


    # Summary Mode

    def summary(self):
        self.print_brief_summary()

    def print_brief_summary(self):
        entries = self.session.query(models.FaereldEntry).count()

        days = self.session.query(models.FaereldEntry.start, models.FaereldEntry.end) \
                    .order_by(models.FaereldEntry.start) \
                    .all()

        total_time = datetime.timedelta(0)

        for index, result in enumerate(days):
            if index == 0:
                first_day = result[0]

            if index == len(days)-1:
                last_day = result[1]

            total_time += result[1] - result[0]

        formatted_time = self._format_time_delta(total_time)

        days = (last_day - first_day).days + 1
        print("\n{0} Days // {1} Entries // {2}".format(days, entries, formatted_time))

    # Insert Mode

    def insert(self):

        self.print_brief_summary()

        print("\n[ Areas :: {0} ]".format(' // '.join(self.areas.keys())))
        area = input('Area :: ').upper()

        if area in self.project_areas:
            object, link = self._project_object()
        else:
            object, link = self._non_project_object()

        # Assume to be in the form [date // time]
        from_date = input('From :: ')
        wending_date, from_date_gregorian = self.convert_input_date(from_date)

        to_date = input('To :: ')
        _, to_date_gregorian = self.convert_input_date(to_date)

        time_diff = self._time_diff(from_date_gregorian, to_date_gregorian)

        if area in self.project_areas:
            project_name = self.config.get_projects()[object]['name']
            print(self.rendering_strings['projects'].format(wending_date.formatted(),
                                                       project_name,
                                                       self.areas[area],
                                                       time_diff))
        else:
            print(self.rendering_strings[area].format(wending_date.formatted(),
                                                 object,
                                                 time_diff))

        confirmation = input("Is this correct? (y/n) :: ")

        if confirmation.lower() == 'y':
            entry = models.FaereldEntry(area=area,
                                        object=object,
                                        link=link,
                                        start=from_date_gregorian,
                                        end=to_date_gregorian)

            self.session.add(entry)
            self.session.commit()
            print("Færeld entry added")
        else:
            print("Færeld entry cancelled")

    def _project_object(self):
        projects = self.config.get_projects()

        print("\n[ Objects :: {0} ]".format(' // '.join(projects.keys())))
        object = input('Object :: ')

        while object not in projects:
            print("\nInvalid Project :: {0}".format(object))
            object = input('Object :: ')

        link = projects[object]['link']
        return (object, link)

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
        return self._format_time_delta(diff_delta)

    def _format_time_delta(self, time_delta):
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes = math.floor(remainder/60)

        return "{0}h{1}m".format(hours, minutes)

    # Sync Mode

    def sync(self):
        print("Sync mode is currently not enabled.")
