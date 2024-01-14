import config
from random import getrandbits


class _OFF:
    @classmethod
    def Reset(this):
        pass

    @classmethod
    def Next(this):
        return 0


class _ON:
    @classmethod
    def Reset(this):
        pass

    @classmethod
    def Next(this):
        return _FULL_MASK


_sequenceList = [
    _OFF,
    _ON,
]


# Returns tuple (SequenceClass, ValidID)
def GetSequence(seqIND):
    seqIND = max(min(seqIND, len(_sequenceList)), 0)
    return (_sequenceList[seqIND], seqIND)


Names = [x.__name__.replace("_", " ") for x in _sequenceList]

_PIN_COUNT = len(config.PINS)
_FULL_MASK = ~(~0 << _PIN_COUNT)
