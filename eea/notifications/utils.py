""" Utils
"""

from eea.rabbitmq.client.rabbitmq_plone import get_rabbitmq_client_settings
from plone import api
import logging

LOGGER = logging.getLogger("eea.notifications")


def list_content_types():
    return api.portal.get_tool(name="portal_types").listContentTypes()


def get_tags(obj):
    try:
        tags = obj.subject
    except Exception:
        tags = ()
    return tags


def get_object_having_path(path):
    """ Usage: path = "/".join(obj.getPhysicalPath())
    """
    try:
        return api.portal.get().unrestrictedTraverse(
            str("/".join(path.split("/")[2:]))  # exclude site root
        )
    except Exception:
        return None


def get_rabbit_config():
    rabbit_client_settings = get_rabbitmq_client_settings()
    rabbit_config = {
        'rabbit_host': rabbit_client_settings.server,
        'rabbit_port': rabbit_client_settings.port,
        'rabbit_username': rabbit_client_settings.username,
        'rabbit_password': rabbit_client_settings.password
        }
    return rabbit_config
