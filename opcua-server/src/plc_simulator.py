from threading import Thread
from opcua import Node
import random
import time

SIGMA_SCALE = 1
INTERVAL = 0.5


class PlcSimulator(Thread):
    def __init__(self, ua_node: Node, operator_id):
        Thread.__init__(self)
        self._stop = False
        self.ua_node = ua_node
        self.operator_id = ua_node.get_child(['3:OperatorId'])
        self.measure_plan_id = ua_node.get_child(['3:MeasurePlanId'])
        self.data_slots = [slot for slot in ua_node.get_child(['3:DataSlot']).get_children()]
        self.state = ua_node.get_child(['3:State'])

        # Init work
        self.operator_id.set_value(operator_id)
        self.state.set_value('ready')

        # Extra info
        parameter_infos = [(2, 3, 1), (2, 3, 1), (2, 3, 1), (2, 3, 1)]
        self.parameters = []
        for item in parameter_infos:
            par = {
                'scale': item[0],
                'cl': (item[1]+item[2])/2,
                'sigma': SIGMA_SCALE*(item[1]-item[2])/6
            }
            self.parameters.append(par)

    def set_measure_plan_id(self, id):
        self.measure_plan_id.set_value(id)

    def stop(self):
        self._stop = True
        self.state.set_value('shut')

    def run(self):
        self.state.set_value('running')
        while not self._stop:
            i = 0
            for par in self.parameters:
                r = round(random.normalvariate(par['cl'], par['sigma']), par['scale'])
                self.data_slots[i].set_value(r)
                i += 1
            time.sleep(INTERVAL)
