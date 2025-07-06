from PySide6.QtCore import Signal, QThread
import subprocess
import time
import uiautomator2 as u2
import threading
from utils import *


class KeepClientInterfaceThread(QThread):
    update_statu_signal = Signal(str)

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.device = None

    def run(self):
        delay = 30
        self.update_statu_signal.emit(f"Keep Client: 将在{delay}'保持客户端界面'功能")
        time.sleep(delay)
        self.update_statu_signal.emit("Keep Client: 启动'保持客户端界面'功能")
        time.sleep(1)

        self.connect_device()

        time.sleep(0.5)
        self.update_statu_signal.emit("Keep Client: 开启循环保持APP界面")
        threading.Thread(target=self.keep_app_run).start()
        time.sleep(0.5)
        self.update_statu_signal.emit("Keep Client: 开启循环保持客户端屏幕常亮")
        threading.Thread(target=self.keep_screen_on).start()

    # 启动线程保持设备常亮
    def keep_screen_on(self):
        while True:
            try:
                self.device.click(10, 50)
            except:
                self.update_statu_signal.emit("Keep Client: 屏幕关闭, 无法点击?")
            time.sleep(29)

    # 启动线程保持出库界面
    def keep_app_run(self):
        app_name = "com.example.myapplication_20250613_outlib_beta08_review"
        while True:
            time.sleep(1)
            try:
                current_app_name = self.device.app_current()["package"]
                if current_app_name != app_name:
                    self.update_statu_signal.emit("Keep Client: 检测到当前APP不是<出库脚本>, 正在切换")
                    self.device.shell(f"am force-stop {app_name}")  # shell强制关闭APP

                    time.sleep(1)
                    self.device.app_start(app_name)
                    self.device.set_orientation("n")  # 保持竖屏
                else:
                    # self.update_statu_signal.emit("current_app_name:", current_app_name)
                    pass
            except:
                self.update_statu_signal.emit("Keep Client: 切换APP失败, 尝试重新连接")
                self.connect_device()

    def connect_device(self):
        try:
            self.update_statu_signal.emit(f"Keep Client: 尝试adb连接:{self.device_id}")
            result = subprocess.run([os.path.join(get_exe_dir(), "asset", "adb.exe"), "connect", self.device_id],
                                    capture_output=True,
                                    text=True,
                                    check=True)
        except subprocess.CalledProcessError as e:
            self.update_statu_signal.emit(f"Keep Client: 无线调试连接安卓设备失败, adb command error:\n{e}")

        while True:
            try:
                self.device = u2.connect(self.device_id)
                self.update_statu_signal.emit(f"Keep Client: 已连接设备:{self.device.device_info['model']}")
                break
            except:
                self.update_statu_signal.emit("Keep Client: 连接设备失败, 尝试重新连接...")
                time.sleep(3)
