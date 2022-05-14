import time
import datetime
import random
from opcua import ua, Node
from threading import Thread, Event

PROD_TIME = 1

MACHINE_STATES = ("运行", "停止", "离线", "故障")
ANTON_STATES1 = ("工作", "坏机", "换机", "计划停机", "损失", "停产")
ANTON_STATES2 = (
    ("工作",),
    ("机器故障", "模具", "工装", "红灯"),
    ("换型", "调整", "工装磨损"),
    ("用餐", "休息", "保养", "交接班", "预热"),
    ("待原料", "待人员", "待工装", "待工具", "待检具", "待文件",
     "待环境", "待指令", "待检验", "待评审", "会议培训", "停水电气"),
    ("无订单", )
)


class Anton:
    def __init__(self, node: Node, idx):
        self.antonObj: Node = node.add_object(idx, 'Anton')
        self.antonState1 = self.antonObj.add_property(
            idx, 'State1', '')
        self.antonState2 = self.antonObj.add_property(
            idx, 'State2', '')
        self.antonDesc = self.antonObj.add_property(idx, 'Description', '')
        self.antonHandle = self.antonObj.add_property(idx, 'Handle', '')
        self.antonBegTime = self.antonObj.add_property(idx, 'BeginTime', '')

    def __set(self, idx1, idx2, h='无', d='无', t=None):
        self.antonState1.set_value(ANTON_STATES1[idx1])
        self.antonState2.set_value(ANTON_STATES2[idx1][idx2])
        self.antonDesc.set_value(d)
        self.antonHandle.set_value(h)
        self.antonBegTime.set_value(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') if t is None else t)

    def set_pause(self):
        self.__set(3, 1)

    def set_working(self):
        self.__set(0, 0)

    def set_offline(self):
        self.__set(5, 0)

    def set_breakdown(self):
        self.__set(1, 0, '待响应')

    def set_repair(self):
        if (self.antonState1.get_value() == '坏机'):
            self.__set(1, 0, '处理中')


class MachineSimulator(Thread):
    def __init__(self, node: Node, idx, config):
        Thread.__init__(self)
        self._terminate = False
        self._pause = True
        self._ctx = Event()
        self.ua_node = node

        # Create nodes
        self.id = node.add_property(idx, 'Id', config['id']).get_value()
        self.measure_plan_id = node.add_property(
            idx, 'MeasurePlanId', config['measure_plan_id']).get_value()
        self.state_node = node.add_property(idx, 'State', '')
        self.plan_node = node.add_variable(
            idx, 'Plan', 0, ua.VariantType.Int32)
        self.done_node = node.add_variable(
            idx, 'Done', 0, ua.VariantType.Int32)

        # Andon
        self.anton = Anton(node, idx)

        # initialize
        self.set_default()

    def set_default(self):
        self.state_node.set_value(MACHINE_STATES[1])
        self.anton.set_pause()
        self.plan_node.set_value(random.randint(2000, 8000))
        self.done_node.set_value(random.randint(200, 800))

    def set_plan(self, p):
        self.plan_node.set_value(p)

    def set_done(self, d):
        self.done_node.set_value(d)

    def activate(self):
        self._pause = False
        self._ctx.set()
        self.state_node.set_value(MACHINE_STATES[0])
        self.anton.set_working()

    def pause(self):
        self._pause = True
        self.state_node.set_value(MACHINE_STATES[1])
        self.anton.set_pause()

    def breakdown(self):
        self._pause = True
        self.state_node.set_value(MACHINE_STATES[3])
        self.anton.set_breakdown()

    def repair(self):
        self.anton.set_repair()

    def terminate(self):
        self._terminate = True
        self.state_node.set_value(MACHINE_STATES[2])

    def run(self):
        while not self._terminate:
            while self.done_node.get_value() < self.plan_node.get_value():
                self.done_node.set_value(
                    self.done_node.get_value()+random.choice([0, 1]))
                time.sleep(PROD_TIME)
                # low possibility to break down
                if (random.randint(1, 3600) == 1500):
                    self.breakdown()

                if self._pause:
                    self._ctx.wait()
                    self._ctx.clear()

            self.set_done(0)
