import os.path
from functools import partial

from outlib_script_ui import Ui_MainWindow

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, \
    QPushButton, QTextEdit, QLineEdit, QCheckBox, QFileDialog
from PySide6.QtCore import Signal, Slot, QThread, Qt

import subprocess
import time
import queue
import threading
import pandas as pd
import socket

from utils_outlib import *
from utils_keep_client import *

from utils import *

# pip install PySide6 uiautomator2 flask soundfile sounddevice pandas opencv-python
"""
init
"""
statu_queue = queue.Queue(50)

"""
广播本机IP
"""
BROADCAST_PORT = 50000
BROADCAST_INTERVAL = 1
BROADCAST_IP = "255.255.255.255"


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接局域网任意主机（不必实际连通）
        s.connect(("192.168.0.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def udp_broadcast_thread():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    lan_ip = get_lan_ip()
    message = lan_ip.encode('utf-8')

    statu_queue.put_nowait("启动UDP广播本机IP")
    while True:
        try:
            sock.sendto(message, (BROADCAST_IP, BROADCAST_PORT))
        except Exception as e:
            statu_queue.put_nowait(f"[广播错误] {e}")
        time.sleep(BROADCAST_INTERVAL)


def load_same_phone_excel(excel_path):
    same_phone_dict = {}
    try:
        df = pd.read_excel(excel_path, dtype=str)
        df.fillna("", inplace=True)
        for index, row in df.iterrows():
            key = row.iloc[0]
            value = ",".join(map(str, row.iloc[1:].values))
            same_phone_dict[key] = value

        statu_queue.put_nowait(f"已加载Excel表格")
        return same_phone_dict
    except:
        statu_queue.put_nowait("加载Excel文件失败，请检测文件路径或内容格式，再重新启动程序！")


def list_android_devices():
    """调用 adb devices 并返回设备 ID 列表"""
    out = subprocess.check_output([os.path.join(get_exe_dir(), "asset", "adb.exe"),
                                   "devices"], text=True)
    ids = [
        line.split()[0] for line in out.splitlines()
        if line.strip() and not line.startswith("List of devices")
    ]
    return ids


class DeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择 Android 设备")
        self.list_widget = QListWidget(self)
        for d in list_android_devices():
            self.list_widget.addItem(QListWidgetItem(d))
        self.list_widget.itemDoubleClicked.connect(self.on_double)
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)

    def on_double(self, item):
        """双击后将选中的 ID 存为属性，并关闭对话框"""
        self.selected_id = item.text()
        self.accept()


class GetQueueQThread(QThread):
    update_statu_singal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                statu = statu_queue.get(timeout=0.01)
                self.update_statu_singal.emit(statu)
            except:
                pass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.checkBox_is_save_outlib_log.setEnabled(False)
        self.lineEdit_outlib_log_path.setEnabled(False)
        self.pushButton_select_outlib_dir.setEnabled(False)

        self.textEdit_running_statu.append("本软件为开源项目，仅供学习与交流使用，开发者不对因使用本软件造成的任何后果承担责任，使用者需自行承担风险。")

        # element
        self.statu_file = "statu"
        self.ui_list = [self.checkBox_is_launch_simulator,
                        self.checkBox_is_save_outlib_log,
                        self.checkBox_is_auto_launch_server,
                        self.checkBox_is_keep_client_app_interface,
                        self.lineEdit_simulator_path,
                        self.lineEdit_outlib_log_path,
                        self.lineEdit_samePhone_path,
                        self.lineEdit_controlled_device_id,
                        self.lineEdit_client_device_id]

        self.init()
        self.get_queue_qthread = GetQueueQThread()
        self.get_queue_qthread.update_statu_singal.connect(self.update_statu)
        self.get_queue_qthread.start()

    def init(self):
        self.load_statu()

        self.pushButton_launch_server.clicked.connect(self.launch_server)
        self.pushButton_view_device_id_list.clicked.connect(self.show_device_id_dialog)
        self.pushButton_select_simulator_path.clicked.connect(partial(self.open_select_file_or_dir_dialog,
                                                                      "*.exe",
                                                                      self.lineEdit_simulator_path))
        self.pushButton_select_samePhone_path.clicked.connect(partial(self.open_select_file_or_dir_dialog,
                                                                      "*.xlsx *.xls",
                                                                      self.lineEdit_samePhone_path))
        self.pushButton_select_outlib_dir.clicked.connect(partial(self.open_select_file_or_dir_dialog,
                                                                  "dir",
                                                                  self.lineEdit_outlib_log_path))
        if self.checkBox_is_auto_launch_server.isChecked():
            self.launch_server()

    def load_statu(self):
        if os.path.exists(self.statu_file):
            statu_list = []
            with open(self.statu_file, "r+") as f:
                statu_list = f.read().split("\n")
            for index, statu in enumerate(statu_list):
                if index < 4:
                    self.ui_list[index].setChecked(statu == "True")
                elif index < len(self.ui_list):
                    self.ui_list[index].setText(statu)

    def save_statu(self):
        with open(self.statu_file, "w+") as f:
            for index, ui in enumerate(self.ui_list):
                if index < 4:
                    f.write(f"{ui.isChecked()}\n")
                else:
                    f.write(f"{ui.text()}\n")

    # 启动服务
    def launch_server(self):
        # 设置UI不可用
        self.set_ui_enable_false()

        self.textEdit_running_statu.append("启动服务中...")
        if self.checkBox_is_keep_client_app_interface.isChecked():
            # 启动 "保持APP界面" 线程
            keep_client_interface_thread = KeepClientInterfaceThread(self.lineEdit_client_device_id.text())
            keep_client_interface_thread.update_statu_signal.connect(self.update_statu)
            keep_client_interface_thread.start()
        # 启动 UDP广播 线程
        threading.Thread(target=udp_broadcast_thread, daemon=True).start()
        same_phone_dict = load_same_phone_excel(self.lineEdit_samePhone_path.text())
        # 启动 "出库" 线程
        outlib_thread = OutlibThread(self.lineEdit_controlled_device_id.text(),
                                     same_phone_dict,
                                     self.checkBox_is_launch_simulator.isChecked(),
                                     self.lineEdit_simulator_path.text())
        outlib_thread.update_statu_signal.connect(self.update_statu)
        outlib_thread.start()

    def show_device_id_dialog(self):
        dlg = DeviceDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self.lineEdit_controlled_device_id.setText(dlg.selected_id)

    def open_select_file_or_dir_dialog(self, ext, line_edit):
        if ext == "dir":
            folder = QFileDialog.getExistingDirectory(
                parent=self,
                caption="选择文件夹",
                dir="",
                options=QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontUseNativeDialog
            )
            if folder:
                line_edit.setText(folder)
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption="选择文件",
                dir="",
                filter=f"Executable Files ({ext});;All Files (*)"
            )
            if file_path:
                line_edit.setText(file_path)

    def closeEvent(self, event, /):
        self.save_statu()
        # 强制结束所有线程, 不安全
        os._exit(0)

    def update_statu(self, statu):
        self.textEdit_running_statu.append(statu)

    def set_ui_enable_false(self):
        for ui in self.ui_list:
            ui.setEnabled(False)
        self.pushButton_select_simulator_path.setEnabled(False)
        self.pushButton_select_samePhone_path.setEnabled(False)
        self.pushButton_view_device_id_list.setEnabled(False)
        self.pushButton_launch_server.setEnabled(False)
        self.checkBox_is_auto_launch_server.setEnabled(True)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
