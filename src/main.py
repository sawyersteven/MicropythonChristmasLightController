import config

import network
import server
import asyncio

import sequencer
import gc

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(dhcp_hostname=config.HOSTNAME)
wlan.connect(config.SSID, config.PASSWORD)

server.Start()
sequencer.Run()

gc.collect()
mainLoop = asyncio.get_event_loop()
mainLoop.run_forever()
