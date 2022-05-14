from PyQt6.QtWidgets import *
from server import UaServer
import sys


class MainWindow(QWidget):
    def __init__(self, server: UaServer):
        super().__init__()
        self.server = server
        self.ops = server.simulator_ops
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # all buttons
        btn1 = QPushButton('开始生产模拟')
        btn2 = QPushButton('暂停生产模拟')
        btn3 = QPushButton('运行测量机器')
        btn4 = QPushButton('暂停测量机器')
        # connect actions
        btn1.clicked.connect(self.ops.run_machine)
        btn2.clicked.connect(self.ops.pause_machine)
        btn3.clicked.connect(lambda: self.ops.measure_continuously(0))
        btn4.clicked.connect(self.ops.set_measure_once)
        # bind to layout
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)

        self.setLayout(layout)
        self.setWindowTitle('OPC UA服务器模拟')
        self.resize(300, 120)
        self.show()

    def closeEvent(self, event):
        self.server.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    server = UaServer()
    server.start()
    window = MainWindow(server)
    sys.exit(app.exec())
