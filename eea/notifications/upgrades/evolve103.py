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

            title_extras = Empty()
            title_extras.doc_attr = 'Title'
            title_extras.index_type = 'Okapi BM25 Rank'
            title_extras.lexicon_id = 'plone_lexicon'

            catalog.addIndex('portal_type', 'FieldIndex')
            catalog.addColumn('portal_type')
            catalog.reindexIndex(('portal_type'), REQUEST=None)
            LOGGER.info("Added 'portal_type' to eea_notifications_catalog.")

            catalog.addIndex('Title', "ZCTextIndex", title_extras)
            catalog.addColumn('Title')
            catalog.reindexIndex(('Title'), REQUEST=None)
            LOGGER.info("Added 'Title' to eea_notifications_catalog.")

            catalog.addIndex('getTags', 'FieldIndex')
            catalog.addColumn('getTags')
            catalog.reindexIndex(('getTags'), REQUEST=None)
            LOGGER.info("Added 'getTags' to eea_notifications_catalog.")
