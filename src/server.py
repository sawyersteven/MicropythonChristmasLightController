import asyncio
from sequencer import GetStatus, SetNewSequence, WriteDefault

import json
import gc
import io
import os
import micropython
import machine
import sys
from nanoweb import HttpError, Nanoweb, send_file, error

try:
    import sequences

    sequenceList = json.dumps(sequences.Names)
except Exception as _:
    sequenceList = json.dumps(["CORRUPT OR MISSING"])


Server = Nanoweb(80)

with open("static/index.html") as f:
    html = f.read().replace("{sequencelist}", sequenceList)

gc.collect()


@Server.route("/")
async def index(request):
    await request.write("HTTP/1.0 200 OK\r\n\r\n")
    await request.write(html)


@Server.route("/script.js")
async def script(request):
    await request.write("HTTP/1.0 200 OK\r\n\r\n")
    await send_file(request, "static/script.js")


@Server.route("/simple.css")
async def simple(request):
    await request.write("HTTP/1.0 200 OK\r\n\r\n")
    await send_file(request, "static/simple.css")


@Server.route("/update")
async def update(request):
    await request.write("HTTP/1.0 200 OK\r\n\r\n")
    await send_file(request, "static/update.html")


@Server.route("/postupdate")
async def pd(request):
    print("pd req")
    if request.method != "POST":
        await request.simple_response(405, "Method Not Allowed")
        return

    OUTPUT_FILE = "sequences.mpy"
    try:
        filesize = bytesleft = int(request.headers.get("Content-Length", 0))
        if not filesize:
            await request.simple_response(204, "No Content")
            return
        if filesize > 4 * 1024:
            await request.simple_response(
                413, f"File size ({filesize/1024}) exceeds limit (4kb)"
            )
            return
    except Exception as e:
        await request.simple_response(500, f"Internal server error ({e})")
        return

    try:
        os.remove(OUTPUT_FILE)
    except Exception as e:
        await request.simple_response(500, f"Internal server error ({e})")
        return

    try:
        with open(OUTPUT_FILE, "wb") as f:
            while bytesleft > 0:
                print(f"{bytesleft}/{filesize}")
                chunk = await request.read(min(bytesleft, 64))
                f.write(chunk)
                bytesleft -= len(chunk)
            f.flush()
    except OSError as e:
        await request.simple_response(500, f"Internal server error ({e})")

    await request.simple_response(200, "Update complete, restarting...")

    print("Rebooting...")
    sys.exit(0)


@Server.route("/test")
async def test(request):
    print("Rebooting...")
    machine.reset()


@Server.route("/status")
async def status(request):
    await request.write(json.dumps(GetStatus()))


@Server.route("/setsequence")
async def setsequence(request):
    if request.method != "POST":
        await request.write("HTTP/1.0 501 Not Implemented\r\n")
        return

    try:
        content_length = int(request.headers["Content-Length"])
    except KeyError:
        await request.write("HTTP/1.0 400 Malformed Data\r\n")
        return

    try:
        data = json.loads((await request.read(content_length)).decode())
        newSeqID = int(data["newSequenceID"])
        newSpd = int(data["newSpeed"])
    except Exception:
        await request.write("HTTP/1.0 400 Malformed Data\r\n")
        return

    SetNewSequence(newSeqID, newSpd)

    await request.write(json.dumps(GetStatus()))
    gc.collect()


@Server.route("/setdefault")
async def setdefault(request):
    if request.method != "POST":
        await request.write("HTTP/1.0 501 Not Implemented\r\n")
        return
    try:
        content_length = int(request.headers["Content-Length"])
    except KeyError:
        await request.write("HTTP/1.0 400 Malformed Data\r\n")
        return

    try:
        data = json.loads((await request.read(content_length)).decode())
        defSeqID = int(data["sequenceID"])
        defSpd = int(data["speed"])
    except Exception:
        await request.write("HTTP/1.0 400 Malformed Data\r\n")
        return

    try:
        (seq, spd) = WriteDefault(defSeqID, defSpd)
        await request.write(json.dumps({"newDefaultSeq": seq, "newDefaultSpeed": spd}))
    except Exception as e:
        await request.write(f"HTTP/1.0 500 {e}\r\n")
        return


@Server.route("/mem")
async def mem(request):
    buff = io.StringIO()
    os.dupterm(buff)
    micropython.mem_info()

    buff.seek(0)
    a = buff.read().strip()
    await request.write(a)


gc.collect()


def Start():
    return asyncio.create_task(
        asyncio.start_server(Server.handle, Server.address, Server.port)
    )
