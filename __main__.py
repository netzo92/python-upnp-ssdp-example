from lib.ssdp import SSDPServer
from lib.upnp_http_server import UPNPHTTPServer
import uuid
import netifaces as ni
from time import sleep
import logging

NETWORK_INTERFACE = 'em0'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_network_interface_ip_address():
    """
    Get the first IP address of a network interface.
    :param interface: The name of the interface.
    :return: The IP address.
    """
    while True:
        network_interface = None
        for potential_network_interface in ni.interfaces():
            if potential_network_interface != 'lo' and potential_network_interface != 'enp1s0' and potential_network_interface != 'enp2s0':
                network_interface = potential_network_interface
            else:
                pass
        if network_interface is None:
            return ""
        interface = ni.ifaddresses(network_interface)
        if (2 not in interface) or (len(interface[2]) == 0):
            return ""
        return interface[2][0]['addr']


device_uuid = uuid.uuid4()
local_ip_address = get_network_interface_ip_address()

http_server = UPNPHTTPServer(8088,
                             friendly_name="NXE 400",
                             manufacturer="Nexa3D",
                             manufacturer_url='https://nexa3d.com/',
                             model_description='NXE 400 3D Printer',
                             model_name="NXE",
                             model_number="400",
                             model_url="https://nexa3d.com/3d-printers/",
                             serial_number="1234",
                             uuid=device_uuid,
                             presentation_url="http://{}:5000/".format(local_ip_address))
http_server.start()

ssdp = SSDPServer()
ssdp.register('local',
              'uuid:{}::upnp:rootdevice'.format(device_uuid),
              'upnp:rootdevice',
              'http://{}:8088/nxe-400.xml'.format(local_ip_address))
ssdp.run()
