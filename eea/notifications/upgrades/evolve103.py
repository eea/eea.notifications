from eea.notifications.catalogtool import get_catalog
from eea.notifications.utils import LOGGER


def run(context):
    """ Configure catalog
    """
    catalog = get_catalog(context)
    if catalog is not None:
        try:
            index = catalog._catalog.getIndex('getTags')
            index = index  # The Happy PEP
        except KeyError:
            catalog.addIndex('getTags', 'FieldIndex')
            LOGGER.info("Added 'getTags' index to eea_notifications_catalog")
