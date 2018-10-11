from Products.CMFPlone.utils import safe_unicode
from binascii import b2a_qp
from eea.notifications.catalogtool import get_catalog
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import six


def safe_encode(value):
    if isinstance(value, six.text_type):
        # no need to use portal encoding for transitional encoding from
        # unicode to ascii. utf-8 should be fine.
        value = value.encode('utf-8')
    return value


def safe_simpleterm_from_value(value):
    return SimpleTerm(value, b2a_qp(safe_encode(value)), safe_unicode(value))


def vocab_from_values(values):
    terms = [safe_simpleterm_from_value(x) for x in values]

    try:
        terms.sort(key=lambda t: t.title)
    except UnicodeDecodeError:
        pass

    vocab = SimpleVocabulary(terms)
    return vocab


@provider(IVocabularyFactory)
def get_tags_vocab(context):
    catalog = get_catalog()
    res = [x[0] for x in catalog.all_tags()]
    vocab = vocab_from_values(res)

    return vocab


@provider(IVocabularyFactory)
def get_events_vocab(context):
    catalog = get_catalog()
    res = [x[0] for x in catalog.all_events()]
    vocab = vocab_from_values(res)

    return vocab
