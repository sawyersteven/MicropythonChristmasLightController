# MicropythonChristmasLightController

## Usage
Modify `config.py` as required.

Build with `python build.py`

This cross-compile any `py` files to `mpy`, minifies `js` and `css`, and runs tests against `sequences.py` to (mostly) ensure the asyncio loop can run without exception.

Copy the contents of `/build` to your controller running MicroPython.

Add the line `import main` to the `boot.py` on your controller.

Reboot.