import machine
import config
import utime
from random import getrandbits
import gc
import asyncio
from micropython import const
import json

try:
    import sequences
except Exception as e:
    import sequences_fallback as sequences


# Responsible for playing sequences and managing state


class SPEED:
    SLOW = const(2000)
    NORMAL = const(1000)
    FAST = const(500)

    @staticmethod
    def constrain(speed):
        return max(min(speed, SPEED.SLOW), SPEED.FAST)


_asyncTask = None
_currentSeqID = 0
_currentSequence = None

_nextExecTick = 0
_currentSpeed = SPEED.NORMAL


# Returns tuple (seqID, speed) with validated values
def WriteDefault(sequenceID, speed):
    speed = SPEED.constrain(speed)
    j = {"seq": sequenceID, "spd": speed}
    json.dump(j, "defaults.json")
    return (sequenceID, speed)


# Returns tuple (seqID, speed)
def ReadDefault():
    try:
        j = json.load("defaults.json")
        seq = j.get("seq", 1)  # Chase_1
        spd = j.get("spd", SPEED.NORMAL)
        return (seq, spd)
    except Exception:
        return (1, SPEED.NORMAL)


def GetStatus():
    return {"nowPlayingID": _currentSeqID, "speed": _currentSpeed}


def SetNewSequence(seqID, speed):
    global _currentSpeed
    global _currentSequence
    global _currentSeqID
    global _asyncTask

    _currentSpeed = SPEED.constrain(speed)
    _currentSeqID = seqID
    _SetSequencer(seqID)
    if _asyncTask is not None:
        _asyncTask.cancel()
        Run()
    pass


def Run():
    print("Starting sequencer")
    global _asyncTask
    loop = asyncio.get_event_loop()
    _asyncTask = loop.create_task(_RunLoop())


async def _RunLoop():
    global _currentSequence
    while True:
        flag = _currentSequence.Next()
        _ApplySequence(flag)
        await asyncio.sleep_ms(_currentSpeed)


def _ApplySequence(flag):
    for pin in config.PINS:
        pin.value(config.TRIGGER == flag & 1)
        flag >>= 1
    print([p.value() for p in config.PINS])


# Validates seqID if out of range, then finds matching sequence function
# Sets global _currentSeqID and global _currentSequence
def _SetSequencer(seqID):
    global _currentSequence
    global _currentSeqID

    (_currentSequence, _currentSeqID) = sequences.GetSequence(_currentSeqID)
    _currentSequence.Reset()
    gc.collect()


SetNewSequence(*ReadDefault())

gc.collect()
