# If sequences.py is missing or corrupted and cannot be imported this will be
# imported instead. This does nothing, but allows the mainloop to run normally
# so that a new sequences.py can be uploaded

Name = ["CORRUPT OR MISSING"]


def GetSequence(seqIND):
    return (_NULLSEQ, 0)


class _NULLSEQ:
    @classmethod
    def Reset(this):
        pass

    @classmethod
    def Next(this):
        return 0b00011000
