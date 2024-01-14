# Runs mpy_cross on every py file in /src and outputs the mpy to /build
import os
import mpy_cross
from time import sleep
import shutil


def cross():
    src = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")

    outDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "build")

    if os.path.isfile(outDir):
        print(f"Output directory `{outDir}` is a file")
        os._exit(0)

    if os.path.isdir(outDir):
        shutil.rmtree(outDir)

    os.mkdir(outDir)

    for file in os.listdir(src):
        if file.endswith(".py"):
            inFile = os.path.join(src, file)
            outFile = os.path.join(
                outDir, os.path.basename(file).split(".")[0] + ".mpy"
            )
            mpy_cross.run(inFile, "-o", outFile)


if __name__ == "__main__":
    cross()
