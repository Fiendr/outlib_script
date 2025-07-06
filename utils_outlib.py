import os.path
from PySide6.QtCore import Signal, Slot, QThread, Qt
from PySide6.QtGui import QPixmap, QImage
import subprocess
import time
import queue
import uiautomator2 as u2
from flask import Flask, render_template, request, jsonify
import threading

import soundfile as sf
import sounddevice as sd
from utils import *


class OutlibThread(QThread):
    update_statu_signal = Signal(str)

    def __init__(self,
                 device_id,
                 same_phone_dict,
                 is_launch_simulator=False,
                 simulator_path=None,
                 host="0.0.0.0",
                 port=5122):
        super().__init__()
        self.device_id = device_id
        self.same_phone_dict = same_phone_dict
        self.is_launch_simulator = is_launch_simulator
        self.simulator_path = simulator_path
        self.host = host
        self.port = port

        self.device = None
        self.app = Flask(__name__)

        # 日志路径
        TODAY = time.strftime("%Y%m%d")  # 日期

        self.TXT_PATH = os.path.join(get_exe_dir(), "asset", "log", f"{TODAY}.txt")

        # 没有则创建
        if not os.path.exists(self.TXT_PATH):
            with open(self.TXT_PATH, "w") as f:
                pass

        """ 音频文件 """
        self.num_dir = os.path.join(get_exe_dir(), "asset", "num_wav")  # 数字音频文件目录
        self.contfind_wav = os.path.join(get_exe_dir(), "asset", "contfind.wav")
        self.same_number_wav = os.path.join(get_exe_dir(), "asset", "same_number.wav")
        self.confirm_full_phone_numbers = os.path.join(get_exe_dir(), "asset", "confirm_full_phone_numbers.wav")

        if self.is_launch_simulator:
            threading.Thread(target=self.launch_simulator, args=(self.simulator_path,)).start()

        # 手机号输入框
        self.phone_input = None
        # 搜索按钮
        self.search_btn = None
        # 清空输入框
        self.clear_phone_input = None
        # 我知道了
        self.i_kown = None
        # 多件“亮灯”
        self.multi_light = None
        # n个待取包裹
        self.multi_package = None
        # 多件 >
        self.multi_icon = None
        # 代收入库
        self.in_lib = None
        # 更多
        self.more = None
        # 更多-亮灯
        self.more_light = None
        # 没有找到
        self.not_find = None

        # 同号
        self.content_page = None
        self.second_line = None
        self.second_line_inlib = None
        self.signed_not_outlib = None

        # 四位手机号 / 六位运单号切换标签
        self.phone_number_tag = None
        self.tracking_number_tag = None

        """ 
        route
        """

        # 路由来返回 HTML 页面
        @self.app.route('/')
        def index():
            return render_template('出库脚本_flask_uiautomator2_beta2.html')

        # 处理表单提交的路由
        @self.app.route('/process_digits', methods=['POST'])
        def process_digits():
            digits = request.form.get('digits')
            self.update_statu_signal.emit(f"接收客户端请求:{digits}")

            if digits == "hello":
                """ 首次连接 """
                return jsonify({"status": "success",
                                "message": "Digits processed successfully",
                                "result": "hello"}), 200
            elif digits and digits.isdigit() and (len(digits) == 4 or len(digits) == 11):
                """四位手机号"""
                # 在这里处理4位数字
                try:
                    # 解析相同手机号
                    same_phone_number_list_str = self.same_phone_dict[digits]
                    self.update_statu_signal.emit(f'"查找到重复号码:", {same_phone_number_list_str}')
                    data, samplerate = sf.read(self.confirm_full_phone_numbers)
                    sd.play(data, samplerate)
                    return jsonify({"status": "success",
                                    "message": "Digits processed successfully",
                                    "result": same_phone_number_list_str}), 200
                except Exception as e:
                    pass
                # save to file and execute job
                now = time.strftime("%Y%m%d-%H%M%S")
                self.update_statu_signal.emit(f"{now} 接收到手机/尾号: [ {digits} ], 已保存到日志文件")
                self.update_statu_signal.emit("[four] --- threading start ---")
                try:
                    threading.Thread(target=self.outlib_script, args=(digits,), daemon=True).start()
                except:
                    self.update_statu_signal.emit("执行线程失败, 尝试重新连接被控端")
                    self.connect_device()
                    self.update_statu_signal.emit("重新执行出库脚本")
                    threading.Thread(target=self.outlib_script, args=(digits,), daemon=True).start()
                    time.sleep(5)

                # 保存文件
                with open(self.TXT_PATH, "a") as f:
                    f.write(f"{now},{digits}\n")
                # 返回一个成功响应
                return jsonify({"status": "success",
                                "message": "Digits processed successfully"}), 200

            elif digits and len(digits) == 5 and digits.isdigit():
                """ 
                五位数 
                sendDigitsToServer(four_num + "0");     //发送一个五位数, 以和四位数区别
                相同号码选择页面, "仅查询后四位"
                """
                digits = digits[:4]
                now = time.strftime("%Y%m%d-%H%M%S")
                self.update_statu_signal.emit(f"{now} 接收到手机/尾号: [ {digits} ], 已保存到日志文件2")
                self.update_statu_signal.emit("[four2] --- threading start ---")
                threading.Thread(target=self.outlib_script, args=(digits,), daemon=True).start()

                # 保存文件
                with open(self.TXT_PATH, "a") as f:
                    f.write(f"{now},{digits}\n")
                # 返回一个成功响应
                return jsonify({"status": "success",
                                "message": "Digits processed successfully"}), 200

            elif digits and len(digits) == 6 and digits.isdigit():
                """六位运单号"""
                self.update_statu_signal.emit("[six] --- threading start ---")
                threading.Thread(target=self.six_tracking_number_start, args=(digits,), daemon=True).start()
                return jsonify({"status": "success", "message": "Digits processed successfully"}), 200

            else:
                # 如果输入无效，返回一个错误响应
                return jsonify({"status": "error", "message": "threading six error"}), 400

    """手机号"""

    def outlib_script(self, num):
        time0 = time.time()

        # 丢设备时, 重连
        try:
            self.phone_input.set_text(num)
        except:
            self.update_statu_signal.emit("输入文本失败, 尝试连接模拟器")
            self.connect_device()
            self.phone_input.set_text(num)

        time.sleep(0.1)
        self.search_btn.click()
        # 没有
        if self.not_find.wait(timeout=1):
            # 播放音频
            data, samplerate = sf.read(self.contfind_wav)
            sd.play(data, samplerate)
            self.update_statu_signal.emit(f'"没有找到1", {time.time() - time0}')
            time.sleep(0.2)
        # 多件
        elif self.multi_light.wait(timeout=0.3):
            """ 如果是 亮灯 """
            self.multi_light.click()

            # """ 如果是 签收 """
            # if multi_package.wait(timeout=0.5):
            #     x1, y1, x2, y2 = multi_package.bounds()
            #     d.click(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2)  # 点击"n个待取包裹"中心点
            #     time.sleep(0.5)
            #     d(text="全部亮灯").click()
            #     time.sleep(0.5)
            #     d(text="我知道了").click()
            #     time.sleep(0.5)
            #     d.press("back")
            #     time.sleep(0.5)

            self.update_statu_signal.emit(f'"找到多件:", {time.time() - time0}')
            time.sleep(0.2)
            try:
                self.i_kown.click()
            except:
                pass
            time.sleep(0.2)
        # 同号
        elif self.second_line_inlib.exists() and (
                self.second_line_inlib.get_text() == "代收入库" or
                self.second_line_inlib.get_text() == "签收未出库"
        ):
            # 先切换窗口
            # 当前窗口已经是 BlueStacks
            # window_name = pyautogui.getActiveWindowTitle()
            # if window_name and "BlueStacks" in window_name:
            # pass
            # else:
            # switch_window("BlueStacks", (0,0,548,949))
            # time.sleep(0.2)
            # 播放语音 号码重复, 请选择
            data, samplerate = sf.read(self.same_number_wav)
            sd.play(data, samplerate)
            self.update_statu_signal.emit("号码重复, 请确认...")

            """ 
            beta4扩展, 重复手机号选择页面 -------------------------------------------------
            """
            # same_phone_queue.put(num)   # 相同手机号放入队列
            # # ---结束---
            return 1
        # 一件
        elif self.more.wait(timeout=0.2):
            self.more.click()
            time.sleep(0.2)
            self.more_light.click()
            self.update_statu_signal.emit(f'"找到1件:", {time.time() - time0}')
            time.sleep(0.2)
            self.i_kown.click()
            time.sleep(0.2)
        # 其它
        else:
            # 播放音频
            data, samplerate = sf.read(self.contfind_wav)
            sd.play(data, samplerate)
            self.update_statu_signal.emit(f'"没有找到2", {time.time() - time0}')
            time.sleep(0.2)

        try:
            # 无论找没找到都清空输入框
            self.clear_phone_input.click()
            self.search_btn.click()
        except:
            self.update_statu_signal.emit("输入间隔太短, 清空输入框失败。")

        return None

    """六位运单号开"""

    def six_tracking_number_start(self, num):
        # 先切换到运单号搜索
        if self.tracking_number_tag.exists():
            self.tracking_number_tag.click()
            time.sleep(0.2)
            # 走正常流程
        self.outlib_script(num)
        time.sleep(0.2)
        # 再切回手机号搜索
        if self.phone_number_tag.exists():
            self.phone_number_tag.click()

    def launch_simulator(self, path):
        try:
            os.startfile(path)
            self.update_statu_signal.emit("正在尝试启动模拟器...")
        except:
            self.update_statu_signal.emit("启动模拟器失败, 请检查文件路径是否正确,或手动启动")

        self.update_statu_signal.emit("等待模拟器启动完成")
        time.sleep(5)

        """启动溪鸟APP"""
        while True:
            time.sleep(2)
            if self.device:
                break

        # todo 改为 app name
        if self.device(text="溪鸟").wait(timeout=60):
            self.update_statu_signal.emit("尝试启动'溪鸟'")
            self.device(text="溪鸟").click()
            time.sleep(3)

        for i in range(100):
            if self.device(text="立即开工").wait(timeout=2):
                self.device(text="立即开工").click()
                time.sleep(2)

            if self.device(text="手机号/取件码/运单号").wait(timeout=2):
                self.device(text="手机号/取件码/运单号").click()
                break

    def init_android_ui(self):
        # 手机号输入框
        self.phone_input = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_input_et")
        # 搜索按钮
        self.search_btn = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_confirm_btn")
        # 清空输入框
        self.clear_phone_input = self.device(resourceId="com.xiniao.andriod.xnapp:id/iv_search_clear")
        # 我知道了
        self.i_kown = self.device(resourceId="com.xiniao.andriod.xnapp:id/ll_bottom_btn_layout")
        # 多件“亮灯”
        self.multi_light = self.device(resourceId="com.xiniao.andriod.xnapp:id/operate_tv")
        # n个待取包裹
        self.multi_package = self.device(resourceId="com.xiniao.andriod.xnapp:id/waybill_num_tv")
        # 多件 >
        self.multi_icon = self.device(resourceId="com.xiniao.andriod.xnapp:id/waybill_num_icon")
        # 代收入库
        self.in_lib = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_waybill_status_tv")
        # 更多
        self.more = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_more_tv")
        # 更多-亮灯
        self.more_light = self.device(resourceId="com.xiniao.andriod.xnapp:id/parcel_bottom_item_tv")
        # 没有找到
        self.not_find = self.device(resourceId="com.xiniao.andriod.xnapp:id/empty_hint_title_tv")

        # 同号
        self.content_page = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_recyclerview")
        self.second_line = self.content_page.child(
            resourceId="com.xiniao.andriod.xnapp:id/search_card_container",
            index=1)
        self.second_line_inlib = self.second_line.child(
            resourceId="com.xiniao.andriod.xnapp:id/search_waybill_status_tv")
        self.signed_not_outlib = self.device(text="签收未出库")

        # 四位手机号 / 六位运单号切换标签
        self.phone_number_tag = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_filter_phone")
        self.tracking_number_tag = self.device(resourceId="com.xiniao.andriod.xnapp:id/search_filter_take_code")

    def run(self):
        time.sleep(1)
        if self.is_launch_simulator:
            # 启动 "启动模拟器" 线程
            threading.Thread(target=self.launch_simulator, args=(self.simulator_path,)).start()
            time.sleep(10)

        self.connect_device()

        self.init_android_ui()
        time.sleep(1)
        self.update_statu_signal.emit("-----------启动Flask服务-----------")
        # 启动 Flask 服务，禁用 reloader，否则会创建两个线程
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def connect_device(self):
        self.update_statu_signal.emit(f"正在尝试连接被控端{self.device_id}...")
        while True:
            try:
                # 连接被控端
                self.device = u2.connect(self.device_id)
                self.update_statu_signal.emit(f"已连接到设备: {self.device.device_info['model']}")
                break
            except Exception as e:
                time.sleep(5)
                self.update_statu_signal.emit(f"连接失败,尝试重新连接...\n{e}")
