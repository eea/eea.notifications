from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


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
    res = ['tag1', 'tag2', 'tag3']
    vocab = vocab_from_values(res)

    return vocab


@provider(IVocabularyFactory)
def get_events_vocab(context):
    res = ['test1', 'test2', 'test3']
    vocab = vocab_from_values(res)

    return vocab
