from cross import cross
from minjs import minjs
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))

import sequences
import sequences_fallback

# I may not ever get around to writing unit tests for this, but these few
# tests will at least make sure the sequences work without throwing an
# exception in the async taskpy

print("Testing sequences")
for i, s in enumerate(sequences._sequenceList):
    print("\t" + s.__name__)
    (seq, _) = sequences.GetSequence(i)
    seq.Reset()
    if not isinstance(seq.Next(), int):
        raise Exception(f"{seq.__name__}.Next() does not return an int")

(seq, _) = sequences_fallback.GetSequence(1)
seq.Reset()
if not isinstance(seq.Next(), int):
    raise Exception(f"{seq.__name__}.Next() does not return an int")

print("Running mpy_cross")
cross()
print("Minifying static")
minjs()
