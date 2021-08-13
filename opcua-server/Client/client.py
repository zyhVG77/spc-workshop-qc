import sys

sys.path.insert(0, "..")

from datetime import datetime
from threading import Thread, Event
from queue import Queue
import numpy as np

from opcua import Client
from IPython import embed


class DataTransmitter(Thread):
    def __init__(self, report_queue, collectors, header, form):
        Thread.__init__(self)
        self._stop = False
        self.report_queue = report_queue
        self.collectors = collectors
        self.header = header
        self.measure_form = form
        self.start_time = None
        self.force = False

    def submit(self, measure_form, subsystem):
        """
        measure_form: the same measure form as in EXAMPLE.py in backend server
        subsystem: measure form belonging to which subsystem, two values: Workshop, Warehouse
        """
        # TODO: Submit measure form to spc server
        pass

    def stop(self):
        self._stop = True

    def run(self):
        count = 0
        while not self._stop:
            self.report_queue.get()
            count += 1
            # All the collector threads have completed their tasks
            if count == self.header['pn']:
                measure_form = {
                    'measure_plan': self.header['mid'],
                    'sample_size': self.header['bz'],
                    'operator_id': self.header['oid'],
                    'start_time': self.start_time,
                    'end_time': datetime.now(),
                    'measure_form': self.measure_form.tolist()
                }
                # print(measure_form)
                self.submit(measure_form, self.header['subsys'])   # Submit to spc server
                count = 0   # reset
                # Wakeup collectors
                for collector in self.collectors:
                    collector.wakeup()


class DataCollector(Thread):
    def __init__(self, idx, feed_queue, report_queue, form, batch_size):
        Thread.__init__(self)
        self._stop = False
        self._ctx = Event()
        self.idx = idx
        self.report_queue = report_queue
        self.feed_queue = feed_queue
        self.batch_size = batch_size
        self.measure_form = form

    def wakeup(self):
        self._ctx.set()

    def run(self):
        while not self._stop:
            for i in range(self.batch_size):
                val = self.feed_queue.get()
                self.measure_form[i, self.idx] = val
            self.report_queue.put(1)
            # Block the thread
            self._ctx.wait()
            self._ctx.clear()


class DataTransmissionHandler:
    def __init__(self, header, indices):
        self.indices = indices
        self.header = header
        self.dirty_filter = np.ones(header['pn'], dtype=int)
        self.buffer_queue = [Queue() for i in range(header['pn'])]
        self.form = np.zeros([header['bz'], header['pn']], dtype=float)

        report_queue = Queue()
        collectors = [DataCollector(
            i, self.buffer_queue[i], report_queue, self.form, header['bz']) for i in range(header['pn'])]
        self.data_transmitter = DataTransmitter(report_queue, collectors, header, self.form)
        self.data_transmitter.start()
        for collector in collectors:
            collector.start()

    def datachange_notification(self, node, val, data):
        if self.indices[node.nodeid] >= 0:
            if self.dirty_filter[self.indices[node.nodeid]]:
                self.dirty_filter[self.indices[node.nodeid]] = 0
            else:
                # Solution to the situation that plc has measured
                # the same value as the previous measurement.
                # If val is -1, that means plc reports such situation
                if val >= 0:
                    self.buffer_queue[self.indices[node.nodeid]].put(val)
        else:
            if val == 'running':
                self.data_transmitter.start_time = datetime.now()

    def event_notification(self, event):
        print("Python: New event", event)


class UaClient(Thread):
    def __init__(self, subsystem):
        Thread.__init__(self)
        # client = Client("opc.tcp://admin@localhost:4840/warehouse/server/") # Connect using a user
        self.client = Client("opc.tcp://localhost:4840/")
        self.subsystem = subsystem
        self.init()

    def init(self):
        _client = self.client
        _client.connect()
        _client.load_type_definitions()
        root = _client.get_root_node()
        uri = "https://github.com/zyhVG77/SpcApp.git"
        idx = _client.get_namespace_index(uri)

        machines = root.get_child(['0:Objects', '{}:{}'.format(idx, self.subsystem)]).get_children()

        # Create one handler for one machine
        handlers = []
        subscriptions = []
        for machine in machines:
            header = {
                'oid': machine.get_child(['{}:OperatorId'.format(idx)]).get_value(),
                'mid': machine.get_child(['{}:MeasurePlanId'.format(idx)]).get_value(),
                'pn': machine.get_child(['{}:ParameterNumber'.format(idx)]).get_value(),
                'bz': machine.get_child(['{}:BatchSize'.format(idx)]).get_value(),
                'subsys': self.subsystem
            }
            parameter_number = header['pn']
            state = machine.get_child(['{}:State'.format(idx)])
            # Get all slots used
            data_slots = [slot for slot in machine.get_child(['{}:DataSlot'.format(idx)]).get_children()][:parameter_number]
            # Create indices for every slot with their number
            indices = {node.nodeid: i for i, node in enumerate(data_slots)}
            # Subscribe machine state change
            indices[state.nodeid] = -1

            handler = DataTransmissionHandler(header, indices)
            for slot in data_slots:
                sub = _client.create_subscription(500, handler).subscribe_data_change(slot)
                subscriptions.append(sub)
            # Subscribe state change
            subscriptions.append(_client.create_subscription(500, handler).subscribe_data_change(state))
            handlers.append(handler)

    def disconnect(self):
        self.client.disconnect()


if __name__ == "__main__":
    client = UaClient('Workshop')
    try:
        embed()
    finally:
        client.disconnect()