# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outlib_script.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(542, 383)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit_running_statu = QTextEdit(self.centralwidget)
        self.textEdit_running_statu.setObjectName(u"textEdit_running_statu")
        self.textEdit_running_statu.setGeometry(QRect(10, 190, 521, 131))
        self.textEdit_running_statu.setAcceptDrops(False)
        self.textEdit_running_statu.setReadOnly(True)
        self.textEdit_running_statu.setOverwriteMode(False)
        self.pushButton_launch_server = QPushButton(self.centralwidget)
        self.pushButton_launch_server.setObjectName(u"pushButton_launch_server")
        self.pushButton_launch_server.setGeometry(QRect(180, 150, 161, 31))
        self.checkBox_is_auto_launch_server = QCheckBox(self.centralwidget)
        self.checkBox_is_auto_launch_server.setObjectName(u"checkBox_is_auto_launch_server")
        self.checkBox_is_auto_launch_server.setGeometry(QRect(350, 160, 101, 19))
        self.lineEdit_client_device_id = QLineEdit(self.centralwidget)
        self.lineEdit_client_device_id.setObjectName(u"lineEdit_client_device_id")
        self.lineEdit_client_device_id.setGeometry(QRect(338, 329, 189, 21))
        self.checkBox_is_keep_client_app_interface = QCheckBox(self.centralwidget)
        self.checkBox_is_keep_client_app_interface.setObjectName(u"checkBox_is_keep_client_app_interface")
        self.checkBox_is_keep_client_app_interface.setGeometry(QRect(10, 330, 322, 19))
        self.checkBox_is_keep_client_app_interface.setCheckable(True)
        self.checkBox_is_keep_client_app_interface.setChecked(False)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 521, 131))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_is_launch_simulator = QCheckBox(self.layoutWidget)
        self.checkBox_is_launch_simulator.setObjectName(u"checkBox_is_launch_simulator")
        self.checkBox_is_launch_simulator.setAcceptDrops(True)
        self.checkBox_is_launch_simulator.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBox_is_launch_simulator)

        self.lineEdit_simulator_path = QLineEdit(self.layoutWidget)
        self.lineEdit_simulator_path.setObjectName(u"lineEdit_simulator_path")

        self.horizontalLayout.addWidget(self.lineEdit_simulator_path)

        self.pushButton_select_simulator_path = QPushButton(self.layoutWidget)
        self.pushButton_select_simulator_path.setObjectName(u"pushButton_select_simulator_path")

        self.horizontalLayout.addWidget(self.pushButton_select_simulator_path)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_is_save_outlib_log = QCheckBox(self.layoutWidget)
        self.checkBox_is_save_outlib_log.setObjectName(u"checkBox_is_save_outlib_log")
        self.checkBox_is_save_outlib_log.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_is_save_outlib_log)

        self.lineEdit_outlib_log_path = QLineEdit(self.layoutWidget)
        self.lineEdit_outlib_log_path.setObjectName(u"lineEdit_outlib_log_path")

        self.horizontalLayout_2.addWidget(self.lineEdit_outlib_log_path)

        self.pushButton_select_outlib_dir = QPushButton(self.layoutWidget)
        self.pushButton_select_outlib_dir.setObjectName(u"pushButton_select_outlib_dir")

        self.horizontalLayout_2.addWidget(self.pushButton_select_outlib_dir)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEdit_samePhone_path = QLineEdit(self.layoutWidget)
        self.lineEdit_samePhone_path.setObjectName(u"lineEdit_samePhone_path")

        self.horizontalLayout_3.addWidget(self.lineEdit_samePhone_path)

        self.pushButton_select_samePhone_path = QPushButton(self.layoutWidget)
        self.pushButton_select_samePhone_path.setObjectName(u"pushButton_select_samePhone_path")

        self.horizontalLayout_3.addWidget(self.pushButton_select_samePhone_path)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.lineEdit_controlled_device_id = QLineEdit(self.layoutWidget)
        self.lineEdit_controlled_device_id.setObjectName(u"lineEdit_controlled_device_id")

        self.horizontalLayout_4.addWidget(self.lineEdit_controlled_device_id)

        self.pushButton_view_device_id_list = QPushButton(self.layoutWidget)
        self.pushButton_view_device_id_list.setObjectName(u"pushButton_view_device_id_list")

        self.horizontalLayout_4.addWidget(self.pushButton_view_device_id_list)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 542, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.textEdit_running_statu.setPlaceholderText("")
        self.pushButton_launch_server.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u670d\u52a1", None))
        self.checkBox_is_auto_launch_server.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u542f\u52a8\u670d\u52a1", None))
        self.lineEdit_client_device_id.setText(QCoreApplication.translate("MainWindow", u"192.168.2.12:5555", None))
        self.checkBox_is_keep_client_app_interface.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u6301\u5ba2\u6237\u7aef\u754c\u9762(\u6bd4\u8f83\u9ebb\u70e6)                    \u5ba2\u6237\u7aef\u8bbe\u5907ID:", None))
        self.checkBox_is_launch_simulator.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u6a21\u62df\u5668    ", None))
        self.lineEdit_simulator_path.setText(QCoreApplication.translate("MainWindow", u"C:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\MuMuPlayer.exe", None))
        self.pushButton_select_simulator_path.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6a21\u62df\u5668\u8def\u5f84", None))
        self.checkBox_is_save_outlib_log.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u51fa\u5e93\u65e5\u5fd7 ", None))
        self.lineEdit_outlib_log_path.setText(QCoreApplication.translate("MainWindow", u"asset\\log", None))
        self.pushButton_select_outlib_dir.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u65e5\u5fd7\u76ee\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u540c\u624b\u673a\u5c3e\u53f7Excel", None))
        self.lineEdit_samePhone_path.setText(QCoreApplication.translate("MainWindow", u"samePhone.xlsx", None))
        self.pushButton_select_samePhone_path.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8868\u683c\u8def\u5f84", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u88ab\u63a7\u5b89\u5353\u8bbe\u5907ID:   ", None))
#if QT_CONFIG(statustip)
        self.lineEdit_controlled_device_id.setStatusTip(QCoreApplication.translate("MainWindow", u"\u6a21\u62df\u5668\u8bf7\u5728\u8bbe\u7f6e\u4e2d\u67e5\u770b, \u624b\u673a\u8bbe\u5907\u8bf7\u4f7f\u7528USB\u8c03\u8bd5\u6a21\u5f0f\u8fde\u63a5\u7535\u8111, \u518d\u70b9\u51fb\"\u67e5\u770b\u8bbe\u7f6eID\u5217\u8868\"\u67e5\u770b.", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_controlled_device_id.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1:7555", None))
        self.lineEdit_controlled_device_id.setPlaceholderText("")
        self.pushButton_view_device_id_list.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u8bbe\u5907ID\u5217\u8868", None))
    # retranslateUi

