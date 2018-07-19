""" Utils
"""

import logging
from plone import api

LOGGER = logging.getLogger("eea.notifications")


def list_content_types():
    return api.portal.get_tool(name="portal_types").listContentTypes()
