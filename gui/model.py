import logging
import collections
import platform_specific
from typing import NamedTuple, Iterator, Tuple, Union, Sequence, Optional, Any

from util.codec import Codec, FileIn, FileOut, namedtupleC, strC, \
        intC, frozensetC, listC, bytesC, tupleC, maybe, \
        enumC, boolC

log = logging.getLogger(__name__)

class PreorderParams(NamedTuple):
    strict : Optional[bool]
    total : Optional[bool]

SIGN = {True: '', False: '¬', None: '?'}
def strPP(p) -> str:
    return '({0}S, {1}T)'.format(
        SIGN[p.strict], SIGN[p.total]
    )

PreorderParamsC = namedtupleC(PreorderParams, maybe(boolC), maybe(boolC))

class PreorderMaximization(NamedTuple):
    p : PreorderParams
    tag : int = 0

class Unattractiveness(NamedTuple):
    p : PreorderParams
    tag : int = 1

class UndominatedChoice(NamedTuple):
    strict : bool
    tag : int = 2

class PartiallyDominantChoice(NamedTuple):
    fc : bool
    tag : int = 3

class StatusQuoUndominatedChoice(NamedTuple):
    tag : int = 4

class Overload(NamedTuple):
    p : PreorderParams
    tag : int = 5

class TopTwo(NamedTuple):
    tag : int = 6

class SequentiallyRationalizableChoice(NamedTuple):
    tag : int = 7

Model = Union[
    PreorderMaximization,
    Unattractiveness,
    UndominatedChoice,
    PartiallyDominantChoice,
    StatusQuoUndominatedChoice,
    Overload,
    TopTwo,
    SequentiallyRationalizableChoice,
]

ModelC = enumC('Model', {
    PreorderMaximization: (PreorderParamsC,),
    Unattractiveness: (PreorderParamsC,),
    UndominatedChoice: (boolC,),
    PartiallyDominantChoice: (boolC,),
    StatusQuoUndominatedChoice: (),
    Overload: (PreorderParamsC,),
    TopTwo: (),
    SequentiallyRationalizableChoice: (),
})

# dicts are ordered from python 3.5 onwards
SPECIAL_NAMES = {
    PreorderMaximization(PreorderParams(total=True, strict=True)):
        'Utility Maximization (strict)',
    PreorderMaximization(PreorderParams(total=True, strict=False)):
        'Utility Maximization (non-strict)',
    Unattractiveness(PreorderParams(total=True, strict=True)):
        'Utility Maximization with an Outside Option (strict)',
    Unattractiveness(PreorderParams(total=True, strict=False)):
        'Utility Maximization with an Outside Option (non-strict)',
    PreorderMaximization(PreorderParams(total=False, strict=True)):
        'Incomplete-Preorder Maximization (strict)',
    PreorderMaximization(PreorderParams(total=False, strict=False)):
        'Incomplete-Preorder Maximization (non-strict)',
    UndominatedChoice(strict=True):
        'Undominated Choice (strict)',
    UndominatedChoice(strict=False):
        'Undominated Choice (non-strict)',
    PartiallyDominantChoice(fc=True):
        'Partially Dominant Choice (forced)',
    PartiallyDominantChoice(fc=False):
        'Partially Dominant Choice (non-forced)',
    StatusQuoUndominatedChoice():
        'Status-Quo-Biased Undominated Choice',
    Overload(PreorderParams(strict=True, total=True)):
        'Overload-Constrained Utility Maximization (strict)',
    Overload(PreorderParams(strict=False, total=True)):
        'Overload-Constrained Utility Maximization (non-strict)',
    TopTwo():
        'Top-Two Choice',
    SequentiallyRationalizableChoice():
        'Sequentially Rationalizable Choice',
}

ORDERING_INDICES = (
    PreorderMaximization(PreorderParams(total=True, strict=True)),
    PreorderMaximization(PreorderParams(total=True, strict=False)),
    Unattractiveness(PreorderParams(total=True, strict=True)),
    Unattractiveness(PreorderParams(total=True, strict=False)),
)

UPPER_BOUND_MODELS = {
    SequentiallyRationalizableChoice(),
}

# returns something comparable
def get_ordering_key(model : Model) -> Any:
    try:
        return ORDERING_INDICES.index(model)
    except ValueError:
        return 1024   # not mentioned

def get_name(model : Model) -> str:
    name = SPECIAL_NAMES.get(model)
    if name:
        return name

    return str(model)

class Category(NamedTuple):
    name : str
    children : Sequence  # recursive types not supported in mypy

class ModelGroup(NamedTuple):
    name: str
    help_url: Optional[str]
    variants: Sequence[Optional[Tuple[str, Model]]]

def mgroup(name: str, help_url: Optional[str]=None, *variants : Optional[Tuple[str, Model]]) -> ModelGroup:
    return ModelGroup(name, help_url, variants)

def preorder(strict: bool=None, total: bool=None) -> Model:
    return PreorderMaximization(PreorderParams(strict, total))

def unattractive(strict: bool=None, total: bool=None) -> Model:
    return Unattractiveness(PreorderParams(strict, total))

def sublabel(main : str, detail : str) -> str:
    return '{0}<br/><small>{1}</small>'.format(main, detail)

MODELS = [
    Category('Choice without a Default Alternative', (
        Category('Forced Choice', (
            mgroup('Utility Maximization',
                'models/fc.html#utility-maximization',
                ('Strict', preorder(strict=True, total=True)),
                ('Non-strict', preorder(strict=False, total=True)),
            ),
            mgroup('Undominated Choice',
                'models/fc.html#incomplete-preference-maximization-undominated-choice',
                ('Strict', UndominatedChoice(strict=True)),
                ('Non-strict', UndominatedChoice(strict=False)),
            ),
            mgroup(sublabel(
                    'Sequentially Rationalizable Choice',
                    '(experimental/partial functionality)',
                ),
                'models/fc.html#sequentially-rationalizable-choice',
                ('Strict', SequentiallyRationalizableChoice()),
                None,
            ),
            mgroup('Top-Two Choice',
                'models/fc.html#top-two-choice',
                ('Strict', TopTwo()),
                None,
            ),
            mgroup('Partially Dominant Choice (forced)',
                'models/fc.html#incomplete-preference-maximization-partially-dominant-choice-forced',
                ('Strict', PartiallyDominantChoice(fc=True)),
                None,
            ),
            # mgroup('Choice with limited attention'),
        )),
        Category('Non-Forced Choice', (
            mgroup('Utility Maximization with an Outside Option',
                'models/nfc.html#utility-maximization-with-an-outside-option',
                ('Strict', unattractive(strict=True, total=True)),
                ('Non-strict', unattractive(strict=False, total=True)),
            ),
            mgroup('Overload-Constrained Utility Maximization',
                'models/nfc.html#overload-constrained-utility-maximization',
                ('Strict', Overload(PreorderParams(strict=True, total=True))),
                ('Non-Strict', Overload(PreorderParams(strict=False, total=True))),
            ),
            mgroup('Maximally Dominant Choice',
                'models/nfc.html#incomplete-preference-maximization-maximally-dominant-choice',
                ('Strict', preorder(strict=True, total=False)),
                ('Non-strict', preorder(strict=False, total=False)),
            ),
            mgroup('Partially Dominant Choice (non-forced)',
                'models/nfc.html#incomplete-preference-maximization-partially-dominant-choice-non-forced',
                ('Strict', PartiallyDominantChoice(fc=False)),
                None,
            ),
        )),
    )),
    Category('Choice with a Default Alternative', (
        mgroup('Status-Quo-Biased Undominated Choice (Bewley model)',
            'models/default.html#status-quo-biased-undominated-choice-bewley-model',
            ('Strict', StatusQuoUndominatedChoice()),
            None,
        ),
    )),
]

def names_in_order() -> Iterator[str]:
    def traverse(item):
        if isinstance(item, Category):
            for child in item.children:
                for name in traverse(child):
                    yield name
        else:
            yield item.name

    for item in MODELS:
        for name in traverse(item):
            yield name