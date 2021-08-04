import sys
sys.path.insert(0, "..")

import logging
from datetime import datetime
from threading import Thread
from queue import Queue
from queue import Empty
import numpy as np

from opcua import Client
from IPython import embed

COLLECTOR_TIMEOUT = 1


class DataCollector(Thread):
    def __init__(self, mid, oid, pn, bz, feed_queue: Queue):
        Thread.__init__(self)
        self.feed_queue = feed_queue
        self._stop = False
        self.mid = mid
        self.oid = oid
        self.batch_size = bz
        self.start_time = None
        self.end_time = None
        self.form = np.zeros([bz+1, pn], dtype=float)
        self.indices = np.zeros(pn, dtype=int)

    def stop(self):
        self._stop = True
        self.end_time = datetime.now()
        # Pre-process the form data
        if self.indices[0] > self.batch_size:
            self.form = self.form[1:].tolist()  # Ignore the dirty data
        else:
            self.form = self.form[:self.batch_size].tolist()

        measure_form = {
            # 'measure_form_id': self.tmpformId,
            'measure_plan': self.mid,
            'sample_size': self.batch_size,
            'operator_id': self.oid,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'measure_form': self.form
        }
        print(measure_form)
        # TODO: Submit to Spc server
        # ...

    def run(self):
        self.start_time = datetime.now()
        while not self._stop or not self.feed_queue.empty():
            try:
                i, value = self.feed_queue.get(timeout=COLLECTOR_TIMEOUT)
                self.form[self.indices[i], i] = value
                self.indices[i] += 1
            except Empty as e:
                continue


class DataTransmissionHandler:
    def __init__(self, header, indices):
        self.dataQueue = Queue()
        self.indices = indices
        self.header = header
        self.collector = None
        self.transmitting = False

    def datachange_notification(self, node, val, data):
        if self.indices[node.nodeid] >= 0:
            self.dataQueue.put((self.indices[node.nodeid], val))
        else:
            if not self.transmitting and val == 'running':
                self.transmitting = True
                self.collector = DataCollector(*self.header, self.dataQueue)
                self.collector.start()
            elif self.transmitting and val == 'shut':
                self.transmitting = False
                self.collector.stop()

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    client = Client("opc.tcp://localhost:4840/warehouse/server/")
    # client = Client("opc.tcp://admin@localhost:4840/warehouse/server/") # Connect using a user

    try:
        client.connect()
        client.load_type_definitions()
        root = client.get_root_node()

        # Getting our namespace idx
        uri = "https://github.com/zyhVG77/SpcApp.git"
        idx = client.get_namespace_index(uri)

        # Get a variable node
        machines = client.get_node('ns=3;i=2002').get_children()

        # Create a handler for every machine
        handlers = []
        subscriptions = []
        for machine in machines:
            header = [
                machine.get_child(['3:OperatorId']).get_value(),
                machine.get_child(['3:MeasurePlanId']).get_value(),
                machine.get_child(['3:ParameterNumber']).get_value(),
                machine.get_child(['3:BatchSize']).get_value()
            ]
            parameter_number = header[2]
            state = machine.get_child(['3:State'])
            # Get all slots used
            data_slots = [slot for slot in machine.get_child(['3:DataSlot']).get_children()][:parameter_number]
            # Number every slot
            indices = {node.nodeid: i for i, node in enumerate(data_slots)}
            # Also subscribe machine state change
            indices[state.nodeid] = -1

            handler = DataTransmissionHandler(header, indices)
            for slot in data_slots:
                sub = client.create_subscription(500, handler).subscribe_data_change(slot)
                subscriptions.append(sub)
            # Subscribe state change
            subscriptions.append(client.create_subscription(500, handler).subscribe_data_change(state))
            handlers.append(handler)

        embed()
    finally:
        client.disconnect()
