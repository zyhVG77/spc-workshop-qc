from opcua import ua, Server, Node
from IPython import embed
import logging
import sys
import json
from plc_simulator import PlcSimulator
from machine_simulator import MachineSimulator

sys.path.insert(0, "..")


PRESET_FILE_PATH = r'D:\School\SpcWorkshop\SpcApp\opcua-server\Server\presets.json'


class SimulationOps:
    def __init__(self, plc_simulators: list, machine_simulators: list):
        self.plc_simulators = plc_simulators
        self.machine_simulators = machine_simulators

    def measure_once(self):
        for s in self.plc_simulators:
            s.activate()

    def measure_continuously(self, idx=0):
        if idx >= 0:
            self.plc_simulators[idx].set_perpetual(True)
            self.plc_simulators[idx].activate()
        else:
            for s in self.plc_simulators:
                s.set_perpetual(True)
                s.activate()

    def set_measure_once(self):
        for s in self.plc_simulators:
            s.set_perpetual(False)

    def pause_measure(self):
        for s in self.plc_simulators:
            s.pause()

    def run_machine(self):
        for m in self.machine_simulators:
            m.activate()

    def pause_machine(self):
        for m in self.machine_simulators:
            m.pause()

    def set_machine_plan(self, i, p):
        if i >= 0:
            self.machine_simulators[i].set_plan(p)
        else:
            for m in self.machine_simulators:
                m.set_plan(p)

    def set_machine_default(self, i):
        if i >= 0:
            self.machine_simulators[i].set_default()
        else:
            for m in self.machine_simulators:
                m.set_default()

    def repair_machine(self):
        for m in self.machine_simulators:
            m.repair()


class UaServer:
    def __init__(self):
        self.server_name = 'UA OPCUA_Server'
        self.endpoint = 'opc.tcp://0.0.0.0:4840/'
        self.uri = 'https://github.com/zyhVG77/SpcApp.git'
        self.server = None
        self.plc_simulators = []
        self.machine_simulators = []
        self.simulator_ops = SimulationOps(
            self.plc_simulators, self.machine_simulators)

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
            config = json.loads(f.read())

        # measure machines
        machines, info = list(config.items())[0]
        folder: Node = _server.nodes.objects.add_folder(idx, machines)
        for device, _info in info.items():
            m: Node = folder.add_object(idx, device)
            simulator = PlcSimulator(m, idx, _info)
            self.plc_simulators.append(simulator)
            simulator.start()

        # product machines
        machines, info = list(config.items())[1]
        folder: Node = _server.nodes.objects.add_folder(idx, machines)
        for device, _info in info.items():
            m: Node = folder.add_object(idx, device)
            simulator = MachineSimulator(m, idx, _info)
            self.machine_simulators.append(simulator)
            simulator.start()

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()


if __name__ == "__main__":
    server = UaServer()
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    ops = server.simulator_ops
    try:
        embed()
    finally:
        server.stop()
