from threading import Thread, Event
from opcua import ua, Node
import random
import time
# import uuid

DATA_SLOT_NUMBER = 10
DATA_SLOT_NUMBERING_START = 0
SIGMA_SCALE = 1
INTERVAL = 2


class PlcSimulator(Thread):
    def __init__(self, node: Node, idx, config):
        Thread.__init__(self)
        self._pause = False
        self._terminate = False
        self._perpetual = False
        self._ctx = Event()

        # Create Nodes
        self.measure_plan_id = node.add_property(
            idx, 'MeasurePlanId', config['measure_plan_id']).get_value()
        # self.operator_id = node.add_property(
        #     idx, 'OperatorId', ''.join(str(uuid.uuid4()).split('-'))).get_value()
        self.operator_id = node.add_property(
            idx, 'OperatorId', str(random.randint(0, 99)).rjust(4, '0')).get_value()
        self.state_node = node.add_property(idx, 'State', 'shut')
        self.parameter_number = node.add_variable(
            idx, 'ParameterNumber', config['parameter_number'], ua.VariantType.Int32).get_value()
        self.batch_size = node.add_variable(
            idx, 'BatchSize', config['batch_size'], ua.VariantType.Int32).get_value()
        slots: Node = node.add_folder(idx, 'DataSlot')
        for i in range(DATA_SLOT_NUMBER):
            slots.add_variable(
                idx, 'v'+str(i+DATA_SLOT_NUMBERING_START), 0, ua.VariantType.Float)

        self.ua_node = node
        self.data_slots = slots.get_children()

        # Extra info & Init
        self.parameter_info = config['parameter_info']
        self.parameters = []
        self.preprocess()

    def preprocess(self):
        for item in self.parameter_info:
            par = {
                'scale': item['scale'],
                'cl': (item['usl'] + item['lsl']) / 2,
                'sigma': SIGMA_SCALE * (item['usl'] - item['lsl']) / 6
            }
            self.parameters.append(par)
        self.state_node.set_value('ready')

    def activate(self):
        self._ctx.set()

    def pause(self):
        self._pause = True

    def terminate(self):
        self._terminate = True
        self.state_node.set_value('shut')

    def set_perpetual(self, perpetual):
        self._perpetual = perpetual

    def run(self):
        while not self._terminate:
            if not self._perpetual:
                # Block the thread
                self._ctx.wait()
                # Prepare for another block
                self._ctx.clear()

            self.state_node.set_value('running')
            countdown = self.batch_size
            while countdown > 0:
                for i, par in enumerate(self.parameters):
                    r = round(random.normalvariate(
                        par['cl'], par['sigma']), par['scale'])
                    # If r is equal to the previous value of the parameter,
                    # ua server WON'T send a message to subscribers to remind the data change
                    if r == self.data_slots[i].get_value():
                        # Use a impossible number to trigger data transmission
                        # Assume that -1 is the impossible number
                        self.data_slots[i].set_value(-1)
                    self.data_slots[i].set_value(r)
                countdown -= 1
                time.sleep(INTERVAL)
            self.state_node.set_value('ready')
