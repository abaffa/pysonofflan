import time
from typing import Dict
from datetime import datetime
from zeroconf import ServiceBrowser, Zeroconf
from pysonofflanr3 import utils


class Discover:
    @staticmethod
    async def discover(logger, seconds_to_wait=5) -> Dict[str, str]:
        """
        :rtype: dict
        :return: Array of devices {"device_id", "ip:port"}
        """
        logger.debug("Looking for all eWeLink devices on local network.")

        zeroconf = Zeroconf()
        listener = MyListener()
        listener.logger = logger
        ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

        time.sleep(seconds_to_wait)

        zeroconf.close()

        return listener.devices


class MyListener:
    def __init__(self):

        self.devices = {}

    def add_service(self, zeroconf, type, name):

        self.logger.debug("%s - Service %s added" % (datetime.now(), name))
        info = zeroconf.get_service_info(type, name)
        self.logger.debug(info)
        device = info.properties[b"id"].decode("ascii")
        ip = utils.parseAddress(info.addresses[0]) + ":" + str(info.port)

        self.logger.info(
            "Found Sonoff LAN Mode device %s at socket %s" % (device, ip)
        )

        self.devices[device] = ip
