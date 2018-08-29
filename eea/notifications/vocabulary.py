from eea.notifications.catalogtool import get_catalog
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


LABELS = {}


def vocab_from_values(values):
    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in values]

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
