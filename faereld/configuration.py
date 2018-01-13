# -*- coding: utf-8 -*-

"""
faereld.configuration
------------------

"""

from os import path, makedirs
import yaml


class Configuration(object):

    # Default Configuration Options

    DEFAULT_DATA_OPTIONS = {
        'data_path': '~/.andgeloman/faereld/data.db',
        'use_wending': False,
        'num_last_objects': 5,
    }

    # Default Sync Options

    DEFAULT_SYNC_OPTIONS = {
        'endpoint': None,
        'api_key': None,
        'batch_size': 50
    }

    # Default Project Areas

    DEFAULT_PROJECT_AREAS = {
        'RES': {
            'name': 'Research',
            'rendering_string': 'On {date} I worked on {object} ({area_name}) for {duration}',
        },
        'DES': {
            'name': 'Design',
            'rendering_string': 'On {date} I worked on {object} ({area_name}) for {duration}',
        },
        'DEV': {
            'name': 'Development',
            'rendering_string': 'On {date} I worked on {object} ({area_name}) for {duration}',
        },
        'DOC': {
            'name': 'Documentation',
            'rendering_string': 'On {date} I worked on {object} ({area_name}) for {duration}',
        },
        'TST': {
            'name': 'Testing',
            'rendering_string': 'On {date} I worked on {object} ({area_name}) for {duration}',
        },
    }

    # Default Projects

    DEFAULT_PROJECTS = {
        'faereld': {
            'name': 'Færeld',
            'link': 'https://github.com/Autophagy/faereld'
        }
    }

    # Default General Areas

    DEFAULT_GENERAL_AREAS = {
        'IRL': {
            'name': 'Real life engagements (confs/talks/meetups)',
            'rendering_string': 'On {date} I was at {object} for {duration}',
            'use_last_objects': False
        },
        'RDG': {
            'name': 'Reading',
            'rendering_string': 'On {date} I read {object} for {duration}',
            'use_last_objects': True
        },
        'LNG': {
            'name': 'Languages',
            'rendering_string': 'On {date} I studied {object} for {duration}',
            'use_last_objects': True
        },
        'TSK': {
            'name': 'Tasks',
            'rendering_string': 'On {date} I worked on {object} for {duration}',
            'use_last_objects': False
        },
    }

    DEFAULT_CONFIG = {
        'data_options': DEFAULT_DATA_OPTIONS,
        'sync_options': DEFAULT_SYNC_OPTIONS,
        'project_areas': DEFAULT_PROJECT_AREAS,
        'projects': DEFAULT_PROJECTS,
        'general_areas': DEFAULT_GENERAL_AREAS
    }

    # The configs defined here must have values set for their defaults.
    # For configs excluded from this group, the defaults are just examples.
    MUST_BE_PRESENT_CONFIGS = ['data_options', 'sync_options']

    # Banner to prepend to the default configuration if it does not exist.

    CONFIG_BANNER = """# Færeld :: Configuration File
#
# Please see
# https://faereld.readthedocs.io/en/latest/usage/configuration.html for a
# complete reference of configuration options, as well as their effects.

"""

    # Headers to prepend each config section

    CONFIG_AREA_HEADERS = {
        'data_options': """# data_options :: Settings For Data Options""",

        'sync_options': """# sync_options :: Settings For Sync Mode
#
# NOTE: Sync mode is currently not implemented, these settings do nothing.""",

        'project_areas': """# project_areas :: Definitions For Project-Specific Areas
#
# Project area definitions should be in the form:
# code:
#   name: Area Name
#   rendering_string: On {date} I worked on {object} for {duration}
#
# See https://faereld.readthedocs.io/en/latest/usage/configuration.html#project-areas for more information.""",

        'projects': """# projects :: Project Object Definitions
#
# A project definition should be of the form
# code:
#   link: <link to project homepage>
#   name: Project Name""",

        'general_areas': """# general_areas :: Definitions For General Areas
#
# Area definitions should be in the form:
# code:
#   name: Area Name
#   rendering_string: On {date} I worked on {object} for {duration}
#   use_last_objects: false
#
# See https://faereld.readthedocs.io/en/latest/usage/configuration.html#general-areas for more information."""
    }

    def __init__(self, configuration_path):
        """ On initialisation, preload the configuration options from the
        defaults.
        """
        self.data_options = self.DEFAULT_DATA_OPTIONS
        self.sync_options = self.DEFAULT_SYNC_OPTIONS
        self.project_areas = self.DEFAULT_PROJECT_AREAS
        self.projects = self.DEFAULT_PROJECTS
        self.general_areas = self.DEFAULT_GENERAL_AREAS
        self.__load_configuration(configuration_path)

    def __load_configuration(self, configuration_path):
        """ Load the configuration from the supplied path. If the file does
        not exist at this path, create it from the default config settings.
        """
        expanded_path = path.expanduser(configuration_path)
        if not path.exists(path.dirname(expanded_path)):
            makedirs(path.dirname(expanded_path))

        if not path.exists(expanded_path):
            self.__write_config_file(expanded_path, self.DEFAULT_CONFIG)
        else:
            self.__load_configuration_values(expanded_path)

    def __load_configuration_values(self, path):
        """ Load the configuration file, update the config values from this
        file.
        """

        config_variables = {
                'data_options': self.data_options,
                'sync_options': self.sync_options,
                'project_areas': self.project_areas,
                'projects': self.projects,
                'general_areas': self.general_areas
            }

        with open(path, 'r') as config_file:
            config_dict = yaml.load(config_file)

            for key, value in config_variables.items():
                self.__update_configuration(key, config_dict, value)

        self.__write_config_file(path, config_variables)


    def __update_configuration(self, config_key, config_dict, var):
        """ Update a config dictionary given a category key
        """
        if config_key in config_dict:
            if config_key in self.MUST_BE_PRESENT_CONFIGS:
                # The values defined in the defaults must be present for these
                # config options.
                var.update(config_dict[config_key])
            else:
                # The values defined in the defaults are just examples, and do
                # not need to be present.
                var.clear()
                var.update(config_dict[config_key])


    def __write_config_file(self, path, config):
        with open(path, 'w') as config_file:

            config_file.write(self.CONFIG_BANNER)

            for key, value in config.items():
                config_file.write(self.CONFIG_AREA_HEADERS[key])
                config_file.write("\n")
                yaml.dump({key: value}, config_file, default_flow_style=False,
                          allow_unicode=True)
                config_file.write("\n")


    def get_data_path(self):
        return self.data_options['data_path']

    def get_use_wending(self):
        return self.data_options['use_wending']

    def get_num_last_objects(self):
        return self.data_options['num_last_objects']

    def get_sync_options(self):
        return self.sync_options

    def get_project_areas(self):
        return self.project_areas

    def get_projects(self):
        return self.projects

    def get_general_areas(self):
        return self.general_areas

    def get_areas(self):
        return {**self.project_areas, **self.general_areas}

