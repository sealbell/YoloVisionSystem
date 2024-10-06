from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import A_windows
import A_sql


class AdminLoginUi(QMainWindow):
    def __init__(self):
        # 鼠标拖动界面设置参数
        self.press_x = 0
        self.press_y = 0
        # 页面生成
        super(AdminLoginUi, self).__init__()
        self.resize(600, 360)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setStyleSheet("QMainWindow{border: 1px solid #303030;}")

        self.label = QLabel(self)
        self.label.setText("基于YOLOv5的小区物业监控目标检测系统")
        self.label.setFixedSize(450, 50)
        self.label.move(0, 0)
        self.label.setStyleSheet("QLabel{background:#303030;}QLabel{color:#ffffff;border:none;font-weight:600;"
                                 "font-size:16px;font-family:'微软雅黑';padding-left:30px}")

        self.exit = QPushButton(self)
        self.exit.setText("☀ 退出系统")
        self.exit.resize(150, 50)
        self.exit.move(450, 0)
        self.exit.setStyleSheet("QPushButton{background:#303030;text-align:center;border:none;font-weight:600;"
                                "color:#909090;font-size:14px;}")
        self.exit.setCursor(Qt.PointingHandCursor)
        self.exit.clicked.connect(self.close)

        self.title = QLabel(self)
        self.title.setText("管理员系统")
        self.title.setFixedSize(600, 40)
        self.title.move(0, 70)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("QLabel{color:#303030;font-weight:600;font-size:30px;font-family:'微软雅黑'; }")

        self.admin_id1 = QLabel(self)
        self.admin_id1.setText("账号")
        self.admin_id1.setFixedSize(60, 40)
        self.admin_id1.move(100, 140)
        self.admin_id1.setAlignment(Qt.AlignCenter)
        self.admin_id1.setStyleSheet(
            " QLabel{color:#303030;border:none;font-weight:600;font-size:25px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.admin_id2 = QLineEdit(self)
        self.admin_id2.setEchoMode(QLineEdit.Normal)  # 正常显示字符
        self.admin_id2.setPlaceholderText("请输入账号...")
        self.admin_id2.setFixedSize(342, 40)
        self.admin_id2.move(158, 140)
        self.admin_id2.setStyleSheet(
            " QLineEdit{padding-left:10px;color:#303030;font-weight:600;font-size:18px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.admin_pwd1 = QLabel(self)
        self.admin_pwd1.setText("密码")
        self.admin_pwd1.setFixedSize(60, 40)
        self.admin_pwd1.move(100, 200)
        self.admin_pwd1.setAlignment(Qt.AlignCenter)
        self.admin_pwd1.setStyleSheet(
             " QLabel{color:#303030;border:none;font-weight:600;font-size:25px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.admin_pwd2 = QLineEdit(self)
        self.admin_pwd2.setEchoMode(QLineEdit.Password)  # 显示密码字符
        self.admin_pwd2.setPlaceholderText("请输入密码...")
        self.admin_pwd2.setFixedSize(342, 40)
        self.admin_pwd2.move(158, 200)
        self.admin_pwd2.setStyleSheet(
            " QLineEdit{padding-left:10px;color:#303030;font-weight:600;font-size:18px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.login_btn = QPushButton(self)
        self.login_btn.setText("登录")
        self.login_btn.resize(190, 50)
        self.login_btn.move(100, 260)
        self.login_btn.setStyleSheet("QPushButton{background:#303030;text-align:center;border:none;font-weight:600;"
                                     "color:#B0B0B0;font-size:25px;border-radius: 25px;}")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.toAdminSystem)

        self.register_btn = QPushButton(self)
        self.register_btn.setText("返回")
        self.register_btn.resize(190, 50)
        self.register_btn.move(310, 260)
        self.register_btn.setStyleSheet("QPushButton{background:#303030;text-align:center;border:none;font-weight:600;"
                                        "color:#B0B0B0;font-size:25px;border-radius: 25px;}")
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.clicked.connect(self.toLogin)

    # ================================ 实现鼠标长按移动窗口功能 ================================ #
    def mousePressEvent(self, event):
        self.press_x = event.x()  # 记录鼠标按下的时候的坐标
        self.press_y = event.y()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()  # 获取移动后的坐标
        if 0 < x < 450 and 0 < y < 50:
            move_x = x - self.press_x
            move_y = y - self.press_y  # 计算移动了多少
            position_x = self.frameGeometry().x() + move_x
            position_y = self.frameGeometry().y() + move_y  # 计算移动后主窗口在桌面的位置
            self.move(position_x, position_y)  # 移动主窗口

    # ================================ 按钮功能函数 ================================ #
    # 去管理系统页面
    def toAdminSystem(self):
        op_mysql = A_sql.OperationMysql()  # 连接数据库
        admin_list = op_mysql.search("select * from admin;")
        login_flag = 0
        admin_id = ""
        admin_pwd = ""
        for i in admin_list:
            if self.admin_id2.text() == i['admin_id'] and self.admin_pwd2.text() == i['admin_pwd']:
                admin_id = i['admin_id']
                admin_pwd = i['admin_pwd']
                login_flag = 1
                break
        self.admin_id2.setText("")
        self.admin_pwd2.setText("")
        if login_flag == 1:
            self.hide()
            A_windows.Windows.admin_system.admin_list = [admin_id, admin_pwd]  # 传入账号密码信息
            A_windows.Windows.admin_system.show()
        else:
            # 创建一个消息框
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("账号或密码错误，请重试!")
            # 显示消息框
            msg_box.exec_()

    # 返回登录页面
    def toLogin(self):
        self.admin_id2.setText("")
        self.admin_pwd2.setText("")
        self.hide()
        A_windows.Windows.login.show()