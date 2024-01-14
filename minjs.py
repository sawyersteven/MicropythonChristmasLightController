from rjsmin import jsmin
import os
import shutil


def minjs():
    srcDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src", "static")
    outDir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "build", "static"
    )

    if os.path.isfile(outDir):
        print(f"Output directory `{outDir}` is a file")
        os._exit(0)

    if os.path.isdir(outDir):
        shutil.rmtree(outDir)

    os.mkdir(outDir)

    for file in os.listdir(srcDir):
        inFile = os.path.join(srcDir, file)
        outFile = os.path.join(outDir, file)
        if file.endswith(".js") or file.endswith(".css"):
            print("Minify " + file)
            textContent = ""
            with open(inFile, "r") as f:
                textContent = f.read()
            textContent = jsmin(textContent)
            with open(outFile, "w") as f:
                f.write(textContent)
        else:
            print("Copying " + file)
            shutil.copyfile(inFile, outFile)


if __name__ == "__main__":
    minjs()
