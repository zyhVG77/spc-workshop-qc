import uuid
import logging
import sys
from plc_simulator import PlcSimulator
import random

sys.path.insert(0, "..")

from IPython import embed
from opcua import ua, uamethod, Server


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """
    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    server = Server()
    # server.disable_clock()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("OPC UA Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        ua.SecurityPolicyType.Basic256Sha256_Sign])

    uri = "SPC Group"
    idx = server.register_namespace(uri)

    # import some nodes from xml
    server.import_xml("../server.xml")

    # starting!
    server.start()

    # Start plc simulation
    machines = server.get_node('ns=3;i=2002').get_children()
    simulators = [PlcSimulator(node, str(random.randint(0,99999999999)).rjust(8,'0')) for node in machines]
    for simulator in simulators:
        simulator.start()

    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        embed()
    finally:
        for simulator in simulators:
            simulator.stop()
        server.stop()
