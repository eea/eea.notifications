""" Utils
"""

from eea.rabbitmq.client.rabbitmq import get_rabbitmq_client_settings
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


def get_rabbit_config():
    rabbit_client_settings = get_rabbitmq_client_settings()
    rabbit_config = {
        'rabbit_host': rabbit_client_settings.server,
        'rabbit_port': rabbit_client_settings.port,
        'rabbit_username': rabbit_client_settings.username,
        'rabbit_password': rabbit_client_settings.password
        }
    return rabbit_config
