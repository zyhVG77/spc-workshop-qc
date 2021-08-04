from threading import Thread
from opcua import Node
import random
import time

SIGMA_SCALE = 1
INTERVAL = 1


class PlcSimulator(Thread):
    def __init__(self, ua_node: Node, operator_id):
        Thread.__init__(self)
        self._stop = False
        self.ua_node = ua_node
        self.operator_id = ua_node.get_child(['3:OperatorId'])
        self.measure_plan_id = ua_node.get_child(['3:MeasurePlanId'])
        self.data_slots = [slot for slot in ua_node.get_child(['3:DataSlot']).get_children()]
        self.state = ua_node.get_child(['3:State'])
        self.parameter_number = ua_node.get_child(['3:ParameterNumber'])
        self.batch_size = ua_node.get_child(['3:BatchSize'])

        # Init work
        self.operator_id.set_value(operator_id)
        self.state.set_value('idle')

        # Extra info
        self.countdown = 0
        self.parameters = []

    def dispatch_task(self, measure_plan_id, batch_size, parameter_number, parameter_infos):
        self.measure_plan_id.set_value(measure_plan_id)
        self.batch_size.set_value(batch_size)
        self.parameter_number.set_value(parameter_number)
        self.countdown = batch_size
        for item in parameter_infos:
            par = {
                'scale': item[0],
                'cl': (item[1] + item[2]) / 2,
                'sigma': SIGMA_SCALE * (item[1] - item[2]) / 6
            }
            self.parameters.append(par)
        self.state.set_value('ready')

    def stop(self):
        self._stop = True
        self.state.set_value('shut')

    def run(self):
        self.state.set_value('running')
        while not self._stop and self.countdown > 0:
            for i, par in enumerate(self.parameters):
                r = round(random.normalvariate(par['cl'], par['sigma']), par['scale'])
                self.data_slots[i].set_value(r)
            self.countdown -= 1
            time.sleep(INTERVAL)

        self.state.set_value('shut')
        time.sleep(2)
        self.state.set_value('ready')
