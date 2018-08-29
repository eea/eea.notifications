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
def get_test_list_vocab(context):
    res = ['test1', 'test2', 'test3']
    vocab = vocab_from_values(res)

    return vocab
