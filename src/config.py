# Pin numbers in order. This is the config for a D1 Mini
PIN_IDS = [5, 4, 0, 2, 14, 12, 13, 15]

# Set to 1 for Trigger High or 0 for Trigger Low relays
TRIGGER = 1

# Network info
SSID = ""
PASSWORD = ""
HOSTNAME = "lightcontroller"

# Don't touch anything below this line
try:
    import machine

    PINS = [machine.Pin(i, machine.Pin.OUT) for i in PIN_IDS]
except Exception:
    PINS = [None] * len(PIN_IDS)
