from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from eea.notifications.catalogtool import get_catalog
from eea.notifications.utils import LOGGER
from plone import api


def run(context):
    """ Configure catalog
    """
    catalog = get_catalog(context)
    if catalog is not None:
        try:
            index = catalog._catalog.getIndex('getTags')
            index = index  # The Happy PEP
        except KeyError:
            class Empty(object):
                """ Empty """
                pass

            elem = []

            word_splitter = Empty()
            word_splitter.group = 'Word Splitter'
            word_splitter.name = 'HTML aware splitter'

            case_normalizer = Empty()
            case_normalizer.group = 'Case Normalizer'
            case_normalizer.name = 'Case Normalizer'

            stop_words = Empty()
            stop_words.group = 'Stop Words'
            stop_words.name = 'Remove listed and single char words'

            elem.append(word_splitter)
            elem.append(case_normalizer)
            elem.append(stop_words)

            catalog.manage_addProduct['ZCTextIndex'].manage_addLexicon(
                'plone_lexicon', 'Default Lexicon', elem)

            catalog.addIndex('getTags', 'KeywordIndex')
            catalog.addColumn('getTags')
            catalog.reindexIndex(('getTags'), REQUEST=None)
            LOGGER.info("Added 'getTags' to eea_notifications_catalog.")

            atct = api.portal.get_tool(name="portal_atct")
            atct.updateIndex(
                        'getTags',
                        friendlyName='getTags',
                        description='getTags description here',
                        enabled=True,
                        criteria='ATSimpleIntCriterion')
            atct.updateMetadata(
                        'getTags',
                        friendlyName='getTags',
                        description='getTags description here',
                        enabled=True)

            at = api.portal.get_tool(name=ARCHETYPETOOLNAME)
            at.setCatalogsByType(
                'MetaType',
                ['portal_catalog', 'eea_notifications_catalog', ]
            )

            catalog.catalog_rebuild()
