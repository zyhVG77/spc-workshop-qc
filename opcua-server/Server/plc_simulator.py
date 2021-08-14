from threading import Thread, Event
from opcua import Node
import random
import time

SIGMA_SCALE = 1
INTERVAL = 1


class PlcSimulator(Thread):
    def __init__(self, ua_node: Node, idx, parameter_info):
        Thread.__init__(self)
        self._pause = False
        self._terminate = False
        self._perpetual = False
        self._ctx = Event()
        self.ua_node = ua_node
        self.data_slots = [slot for slot in ua_node.get_child(['{}:DataSlot'.format(idx)]).get_children()]
        self.state = ua_node.get_child(['{}:State'.format(idx)])
        self.parameter_number = ua_node.get_child(['{}:ParameterNumber'.format(idx)]).get_value()
        self.batch_size = ua_node.get_child(['{}:BatchSize'.format(idx)]).get_value()

        # Extra info & Init
        self.parameter_info = parameter_info
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
        self.state.set_value('ready')

    def activate(self):
        self._ctx.set()

    def pause(self):
        self._pause = True

    def terminate(self):
        self._terminate = True
        self.state.set_value('shut')

    def set_perpetual(self, perpetual):
        self._perpetual = perpetual

    def run(self):
        while not self._terminate:
            if not self._perpetual:
                # Block the thread
                self._ctx.wait()
                # Prepare for another block
                self._ctx.clear()

            self.state.set_value('running')
            countdown = self.batch_size
            while countdown > 0:
                for i, par in enumerate(self.parameters):
                    r = round(random.normalvariate(par['cl'], par['sigma']), par['scale'])
                    # If r is equal to the previous value of the parameter,
                    # ua server WON'T send a message to subscribers to remind the data change
                    if r == self.data_slots[i].get_value():
                        # Use a impossible number to trigger data transmission
                        self.data_slots[i].set_value(-1)    # Assume that -1 is the impossible number
                    self.data_slots[i].set_value(r)
                countdown -= 1
                time.sleep(INTERVAL)
            self.state.set_value('ready')
