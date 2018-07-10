""" EEA Notifications package
"""

from zope.i18nmessageid import MessageFactory
from Products.CMFPlone.utils import ToolInit

from eea.notifications.catalogtool import EEANotificationsCatalogTool

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('eea.notifications')

tools = (EEANotificationsCatalogTool,)


def initialize(context):
    # Register our custom catalog tool
    ToolInit('EEA Notifications Catalog Tool',
             tools=tools,
             icon='tool.gif',
             ).initialize(context)
