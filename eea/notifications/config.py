""" Configuration
"""

import os


def ENVPATH(name, default=None):
    """ GET path from os env
    """
    path = os.environ.get(name)
    if not path and default is None:
        raise EnvironmentError('{} needs to be defined!'.format(name))
    else:
        return path or default


ENV_HOST_NAME = ENVPATH(
    'EEA_NOTIFICATIONS_ENV_HOST_NAME', 'climate-adapt.eea.europa.eu')

ENV_PLONE_NAME = ENVPATH(
    'EEA_NOTIFICATIONS_ENV_PLONE_NAME', '/cca')

ANNOT_TAGS_KEY = "eea.notifications.tags"
ANNOT_EVENTS_KEY = "eea.notifications.events"

OBJECT_EVENTS = [
    'added',
    'modified',
    'deleted',
]
