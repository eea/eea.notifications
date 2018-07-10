""" The Notifications catalog
    Global persistent utility that holds the catalog
"""

from Globals import InitializeClass
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFPlone.CatalogTool import CatalogTool


class EEANotificationsCatalogTool(CatalogTool):

    id = 'eea_notifications_catalog'
    meta_type = 'EEA Notifications Catalog Tool'

    def __init__(self):
        ZCatalog.__init__(self, self.getId())


InitializeClass(EEANotificationsCatalogTool)
