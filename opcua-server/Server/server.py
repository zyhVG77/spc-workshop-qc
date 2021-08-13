import uuid
import logging
import sys
import json
from plc_simulator import PlcSimulator

sys.path.insert(0, "..")

from IPython import embed
from opcua import ua, Server, Node

PRESET_FILE_PATH = 'presets.json'
DATA_SLOT_NUMBER = 10
DATA_SLOT_NUMBERING_START = 0


class UaServer:
    def __init__(self):
        self.server_name = 'UA Server'
        self.endpoint = 'opc.tcp://0.0.0.0:4840/'
        self.uri = 'https://github.com/zyhVG77/SpcApp.git'
        self.server = None
        self.measure_plan_infos = None
        self.data_slot_number = DATA_SLOT_NUMBER
        self.simulators = dict()

        self.build_server()

    def build_server(self):
        self.server = Server()
        _server = self.server
        _server.set_endpoint(self.endpoint)
        _server.set_server_name(self.server_name)
        # set all possible endpoint policies for clients to connect through
        _server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])
        idx = _server.register_namespace(self.uri)
        logging.basicConfig(level=logging.WARN)

        # Load parameters & Create simulators
        with open(PRESET_FILE_PATH, 'r', encoding='utf-8') as f:
            self.measure_plan_infos = json.loads(f.read())
        # Create node for every machine in every subsystem
        for subsys, info in self.measure_plan_infos.items():
            folder: Node = _server.nodes.objects.add_folder(idx, subsys)

            if subsys not in self.simulators:
                self.simulators[subsys] = []

            for device, _info in info.items():
                m: Node = folder.add_object(idx, device)
                m.add_property(idx, 'MeasurePlanId', _info['measure_plan_id'])
                m.add_property(idx, 'OperatorId', ''.join(str(uuid.uuid4()).split('-')))
                m.add_property(idx, 'State', 'shut')
                m.add_variable(idx, 'ParameterNumber', _info['parameter_number'], ua.VariantType.Int32)
                m.add_variable(idx, 'BatchSize', _info['batch_size'], ua.VariantType.Int32)
                data_slots: Node = m.add_folder(idx, 'DataSlot')
                for i in range(self.data_slot_number):
                    data_slots.add_variable(idx, 'v'+str(i+DATA_SLOT_NUMBERING_START), 0, ua.VariantType.Float)
                # Create one simulator for one machine
                simulator = PlcSimulator(m, idx, _info['parameter_info'])
                self.simulators[subsys].append(simulator)
                simulator.start()

    def assign_task(self, sub_sys_name, perpetual=False):
        for simulator in self.simulators[sub_sys_name]:
            simulator.set_perpetual(perpetual)
            simulator.activate()

    def clear_perpetual_simulation(self, sub_sys_name):
        for simulator in self.simulators[sub_sys_name]:
            simulator.set_perpetual(False)

    def pause_simulation(self):
        for simulator in self.simulators['Workshop']:
            simulator.pause()

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()


if __name__ == "__main__":
    server = UaServer()
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        embed()
    finally:
        server.stop()
