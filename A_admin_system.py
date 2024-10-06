import os
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import A_sql


class AdminSystemUi(QMainWindow):
    def __init__(self):
        # 鼠标拖动界面设置参数
        self.press_x = 0
        self.press_y = 0
        # 页面参数
        self.identify_record = []  # 查询记录
        self.identify_record_path = ""  # 图像路径
        self.users_list = []  # 所有用户账户
        self.admin_list = []  # 账号密码
        self.functions = []  # 左侧按钮列表
        self.function_flag = 1  # 目前按钮标识
        self.right_widgets = []  # 右侧界面列表
        # 页面生成
        super(AdminSystemUi, self).__init__()
        self.resize(1400, 720)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setStyleSheet("QMainWindow{border: 1px solid #303030;}")

        self.label = QLabel(self)
        self.label.setText("基于YOLOv5的小区物业监控目标检测系统")
        self.label.setFixedSize(1250, 60)
        self.label.move(0, 0)
        self.label.setStyleSheet("QLabel{background:#303030;}QLabel{color:#ffffff;border:none;font-weight:600;"
                                 "font-size:16px;font-family:'微软雅黑';padding-left:30px}")

        self.exit = QPushButton(self)
        self.exit.setText("☀ 退出系统")
        self.exit.resize(150, 60)
        self.exit.move(1250, 0)
        self.exit.setStyleSheet("QPushButton{background:#303030;text-align:center;border:none;font-weight:600;"
                                "color:#909090;font-size:14px;}")
        self.exit.setCursor(Qt.PointingHandCursor)
        self.exit.clicked.connect(self.close)
        # 左侧文本显示区
        self.function_label = QLabel(self)
        self.function_label.setText("管理员后台")
        self.function_label.setFixedSize(219, 220)
        self.function_label.move(1, 60)
        self.function_label.setAlignment(Qt.AlignCenter)
        self.function_label.setStyleSheet(
            "QLabel{background:#ffffff;color:#2c3a45;border:none;font-weight:600;font-size:20px;font-family:'微软雅黑';}")
        # 左侧按钮1
        self.function1 = QPushButton(self)
        self.function1.setText("❤  检测查询")
        self.function1.resize(219, 70)
        self.function1.move(1, 280)
        self.function1.setStyleSheet(
            "QPushButton{background:#e6e6e6;color:#2c3a45;text-align:left;padding-left:50px;"
            "border:none;font-weight:600;font-size:15px;font-family:'微软雅黑';}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.function1.setCursor(Qt.PointingHandCursor)
        self.function1.clicked.connect(
            lambda: self.change_button(self.functions[self.function_flag - 1], self.function1, 1))
        # 左侧按钮2
        self.function2 = QPushButton(self)
        self.function2.setText("❤  用户管理")
        self.function2.resize(219, 70)
        self.function2.move(1, 350)
        self.function2.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;text-align:left;padding-left:50px;"
            "border:none;font-weight:600;font-size:15px;font-family:'微软雅黑';}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.function2.setCursor(Qt.PointingHandCursor)
        self.function2.clicked.connect(
            lambda: self.change_button(self.functions[self.function_flag - 1], self.function2, 2))
        # 左侧按钮3
        self.function3 = QPushButton(self)
        self.function3.setText("❤  账号管理")
        self.function3.resize(219, 70)
        self.function3.move(1, 420)
        self.function3.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;text-align:left;padding-left:50px;"
            "border:none;font-weight:600;font-size:15px;font-family:'微软雅黑';}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.function3.setCursor(Qt.PointingHandCursor)
        self.function3.clicked.connect(
            lambda: self.change_button(self.functions[self.function_flag - 1], self.function3, 3))
        # 左侧下方补白区
        self.function_label2 = QLabel(self)
        self.function_label2.setFixedSize(219, 229)
        self.function_label2.move(1, 490)
        self.function_label2.setStyleSheet("QLabel{background:#ffffff;}")
        # ===== 右侧界面1 ===== #
        self.right_widget1 = QWidget(self)
        self.right_widget1.resize(1179, 659)
        self.right_widget1.move(220, 60)
        # 日期显示框
        self.date_show = QLabel(self.right_widget1)
        self.date_show.setText("--")
        self.date_show.setFixedSize(350, 40)
        self.date_show.move(40, 20)
        self.date_show.setAlignment(Qt.AlignCenter)
        self.date_show.setStyleSheet(
            " QLabel{padding-left:10px;color:#303030;font-weight:600;font-size:15px;border: 2px solid #000000;"
            "font-family:'微软雅黑'; }")
        # 选择日期按钮
        self.button_date = QPushButton(self.right_widget1)  # 查询
        self.button_date.setText("日期查询")
        self.button_date.resize(152, 40)
        self.button_date.move(388, 20)
        self.button_date.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;font-weight:600;font-size:18px;"
            "font-family:'微软雅黑';border:2px solid #000000;}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.button_date.setCursor(Qt.PointingHandCursor)
        self.button_date.clicked.connect(self.select_record_by_date)
        # 全部查询按钮
        self.button_select = QPushButton(self.right_widget1)  # 查询
        self.button_select.setText("全部查询")
        self.button_select.resize(150, 40)
        self.button_select.move(590, 20)
        self.button_select.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;font-weight:600;font-size:18px;"
            "font-family:'微软雅黑';border:2px solid #000000;}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.button_select.setCursor(Qt.PointingHandCursor)
        self.button_select.clicked.connect(self.select_all_record)
        # 删除按钮
        self.button_delete = QPushButton(self.right_widget1)  # 删除
        self.button_delete.setText("删除记录")
        self.button_delete.resize(350, 40)
        self.button_delete.move(790, 20)
        self.button_delete.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;font-weight:600;font-size:18px;"
            "font-family:'微软雅黑';border:2px solid #000000;}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.button_delete.setCursor(Qt.PointingHandCursor)
        self.button_delete.clicked.connect(self.del_record)
        # 表格
        self.table_view = QTableWidget(self.right_widget1)
        self.table_view.setFocusPolicy(Qt.NoFocus)
        self.table_view.resize(1100, 560)
        self.table_view.move(40, 80)
        self.table_view.setColumnCount(6)
        self.table_view.setHorizontalHeaderLabels(['编号', '用户ID', '场景', '名称', '检测时间', '查看'])
        self.table_view.verticalHeader().setVisible(False)  # 隐藏列头
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑表格内容
        header = self.table_view.horizontalHeader()  # 获取表头
        header.setSectionResizeMode(QHeaderView.Stretch)  # 使表头自适应宽度
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选择行为选择一行单元格
        self.table_view.setStyleSheet("QTableWidget{color:#555555;font-size:15px;border:2px solid #000000;"
                                      "font-weight:bold;font-family:'黑体';}")
        self.reset1()
        self.select_all()
        self.show_table()
        # ===== 右侧界面2 ===== #
        self.right_widget2 = QWidget(self)
        self.right_widget2.resize(1179, 659)
        self.right_widget2.move(220, 55)
        # 审核按钮
        self.button_agree = QPushButton(self.right_widget2)  # 同意注册
        self.button_agree.setText("同意注册")
        self.button_agree.resize(250, 40)
        self.button_agree.move(590, 20)
        self.button_agree.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;font-weight:600;font-size:18px;"
            "font-family:'微软雅黑';border:2px solid #000000;}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.button_agree.setCursor(Qt.PointingHandCursor)
        self.button_agree.clicked.connect(self.agree_user)
        # 删除按钮
        self.button_delete2 = QPushButton(self.right_widget2)  # 删除
        self.button_delete2.setText("注销账号")
        self.button_delete2.resize(250, 40)
        self.button_delete2.move(890, 20)
        self.button_delete2.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;font-weight:600;font-size:18px;"
            "font-family:'微软雅黑';border:2px solid #000000;}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.button_delete2.setCursor(Qt.PointingHandCursor)
        self.button_delete2.clicked.connect(self.delete_user)
        # 表格
        self.table_view2 = QTableWidget(self.right_widget2)
        self.table_view2.setFocusPolicy(Qt.NoFocus)
        self.table_view2.resize(1100, 560)
        self.table_view2.move(40, 80)
        self.table_view2.setColumnCount(2)
        self.table_view2.setHorizontalHeaderLabels(['用户ID', '注册状态'])
        self.table_view2.verticalHeader().setVisible(False)  # 隐藏列头
        self.table_view2.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑表格内容
        header = self.table_view2.horizontalHeader()  # 获取表头
        header.setSectionResizeMode(QHeaderView.Stretch)  # 使表头自适应宽度
        self.table_view2.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选择行为选择一行单元格
        self.table_view2.setStyleSheet("QTableWidget{color:#555555;font-size:15px;border:2px solid #000000;"
                                       "font-weight:bold;font-family:'黑体';}")
        self.right_widget2.hide()

        # ===== 右侧界面3 ===== #
        self.right_widget3 = QWidget(self)
        self.right_widget3.resize(1179, 659)
        self.right_widget3.move(220, 55)
        self.admin_id1 = QLabel(self.right_widget3)
        self.admin_id1.setText("账号")
        self.admin_id1.setFixedSize(150, 40)
        self.admin_id1.move(100, 40)
        self.admin_id1.setAlignment(Qt.AlignCenter)
        self.admin_id1.setStyleSheet(
            " QLabel{color:#303030;border:none;font-weight:600;font-size:25px;font-family:'微软雅黑'; "
            "border: 2px solid #000000;}")

        self.admin_id2 = QLabel(self.right_widget3)
        self.admin_id2.setFixedSize(832, 40)
        self.admin_id2.move(248, 40)
        self.admin_id2.setStyleSheet(
            " QLabel{padding-left:10px;color:#303030;font-weight:600;font-size:18px;font-family:'微软雅黑'; "
            "border: 2px solid #000000; background:#ffffff;}")
        self.admin_pwd1 = QLabel(self.right_widget3)
        self.admin_pwd1.setText("密码")
        self.admin_pwd1.setFixedSize(150, 40)
        self.admin_pwd1.move(100, 100)
        self.admin_pwd1.setAlignment(Qt.AlignCenter)
        self.admin_pwd1.setStyleSheet(
            " QLabel{color:#303030;border:none;font-weight:600;font-size:25px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.admin_pwd2 = QLineEdit(self.right_widget3)
        self.admin_pwd2.setEchoMode(QLineEdit.Normal)
        self.admin_pwd2.setFixedSize(832, 40)
        self.admin_pwd2.move(248, 100)
        self.admin_pwd2.setStyleSheet(
            " QLineEdit{padding-left:10px;color:#303030;font-weight:600;font-size:18px;font-family:'微软雅黑'; border: 2px solid #000000;}")

        self.upd_btn = QPushButton(self.right_widget3)
        self.upd_btn.setText("修改密码")
        self.upd_btn.resize(980, 50)
        self.upd_btn.move(100, 160)
        self.upd_btn.setStyleSheet("QPushButton{;text-align:center;border:2px solid #000000;font-weight:600;"
                                   "font-size:25px;border-radius: 25px;}"
                                   "QPushButton:hover{background:#e6e6e6;}")
        self.upd_btn.setCursor(Qt.PointingHandCursor)
        self.upd_btn.clicked.connect(self.upd_password)
        self.right_widget3.hide()

        #  左边列表按钮列表和右边界面列表
        self.functions = [self.function1, self.function2, self.function3]
        self.right_widgets = [self.right_widget1, self.right_widget2, self.right_widget3, self.right_widget1]

    # ================================ 实现鼠标长按移动窗口功能 ================================ #
    def mousePressEvent(self, event):
        self.press_x = event.x()  # 记录鼠标按下的时候的坐标
        self.press_y = event.y()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()  # 获取移动后的坐标
        if 0 < x < 1050 and 0 < y < 60:
            move_x = x - self.press_x
            move_y = y - self.press_y  # 计算移动了多少
            position_x = self.frameGeometry().x() + move_x
            position_y = self.frameGeometry().y() + move_y  # 计算移动后主窗口在桌面的位置
            self.move(position_x, position_y)  # 移动主窗口

    # ================================ 函数区域 ================================#
    # 点击列表按钮切换界面和切换按钮颜色
    def change_button(self, button_1, button_2, flag):
        button_1.setStyleSheet(
            "QPushButton{background:#ffffff;color:#2c3a45;text-align:left;padding-left:50px;"
            "border:none;font-weight:600;font-size:15px;font-family:'微软雅黑';}"
            "QPushButton:hover{background:#e6e6e6;}")
        button_2.setStyleSheet(
            "QPushButton{background:#e6e6e6;color:#2c3a45;text-align:left;padding-left:50px;"
            "border:none;font-weight:600;font-size:15px;font-family:'微软雅黑';}"
            "QPushButton:hover{background:#e6e6e6;}")
        self.right_widgets[self.function_flag - 1].hide()  # 隐藏界面
        self.right_widgets[flag - 1].show()  # 显示界面
        self.function_flag = flag
        if flag == 1:
            self.reset1()
            self.select_all()
            self.show_table()
        if flag == 2:
            self.select_all2()
            self.show_table2()
        if flag == 3:
            self.show_admin()

    # ========== 检测管理相关函数 =============
    # 获取所有当前用户对应的检测记录
    def select_all(self):
        op_mysql = A_sql.OperationMysql()
        self.identify_record = op_mysql.search("select * from records;")

    # 显示数据
    def show_table(self):
        self.table_view.setRowCount(len(self.identify_record))  # 行
        for i in range(len(self.identify_record)):
            checkbox = QCheckBox()
            checkbox.setStyleSheet("padding-left:5px;")
            self.table_view.setCellWidget(i, 0, checkbox)
            self.table_data(self.table_view, i, 0, self.identify_record[i]['record_id'])
            self.table_data(self.table_view, i, 1, self.identify_record[i]['record_user_id'])
            self.table_data(self.table_view, i, 2, self.identify_record[i]['record_scene'])
            self.table_data(self.table_view, i, 3, self.identify_record[i]['record_name'])
            self.table_data(self.table_view, i, 4, self.identify_record[i]['record_time'])
            table_btn = QPushButton('查看')
            table_btn.setCursor(Qt.PointingHandCursor)
            table_btn.setStyleSheet(
                "QPushButton{background:#dddddd;color:#2c3a45;font-weight:600;margin:5px;"
                "font-size:15px;font-family:'微软雅黑';border-radius:14px;border: 2px solid #000000;}"
                "QPushButton:hover{background:#e6e6e6;}")
            self.table_view.setCellWidget(i, 5, table_btn)
            table_btn.clicked.connect(
                lambda _, record_path=self.identify_record[i]['record_name']: self.record_show(record_path))

    # 返回表格填充页面
    @staticmethod
    def table_data(table, i, j, data):
        table.setRowHeight(i, 40)  # 设置高40
        item = QTableWidgetItem()
        table.setItem(i, j, item)
        item = table.item(i, j)
        item.setText(str(data))
        item.setToolTip(str(data))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 水平垂直居中

    # 查询所有记录
    def select_all_record(self):
        self.date_show.setText("--")
        self.select_all()
        self.show_table()

    # 按日期查询
    def select_record_by_date(self):
        picker = DateWin()
        if picker.exec_() == QDialog.Accepted:
            selected_date = picker.calendar.selectedDate()
            year = str(selected_date.year())
            month = str(selected_date.month())
            day = str(selected_date.day())
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            date_result = year + "-" + month + "-" + day
            op_mysql = A_sql.OperationMysql()
            record_list = op_mysql.search("select * from records where record_time like '" + date_result + "%';")
            if len(record_list) != 0:
                self.identify_record = record_list
                self.date_show.setText(date_result)
                self.show_table()
            else:
                # 创建一个消息框
                msg_box = QMessageBox()
                msg_box.setWindowTitle("提示")
                msg_box.setText("没有该天记录，查询失败！")
                # 显示消息框
                msg_box.exec_()

    # 批量删除
    def del_record(self):
        select_list = []
        for i in range(self.table_view.rowCount()):
            item = self.table_view.cellWidget(i, 0)
            if item.isChecked():
                select_list.append(self.identify_record[i])
        if len(select_list) == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("请先选择要删除的记录！")
            msg_box.exec_()
        else:
            for i in select_list:
                if i['record_name'][0:1] == 'v':
                    os.remove("./A_output/videos/" + i['record_name'])
                elif i['record_name'][0:1] == 'c':
                    os.remove("./A_output/camera/" + i['record_name'])
                elif i['record_name'][0:1] == 'i':
                    os.remove("./A_output/images/" + i['record_name'])
                op_mysql = A_sql.OperationMysql()
                op_mysql.delete_one("delete from records where record_id='" + str(i['record_id'])+ "'")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("删除成功！")
            msg_box.exec_()
            if self.date_show.text() == "--":
                self.select_all()
            else:
                op_mysql = A_sql.OperationMysql()
                self.identify_record = op_mysql.search("select * from records where record_time like '" + self.date_show.text() + "%';")
        self.show_table()

    # 查看结果
    def record_show(self, path):
        if path[0:1] == 'v':
            self.identify_record_path = "./A_output/videos/" + path
        elif path[0:1] == 'c':
            self.identify_record_path = "./A_output/camera/" + path
        else:
            self.identify_record_path = "./A_output/images/" + path
        if self.identify_record_path[-3:] == "jpg":
            image_win = ImageWin(self)
            image_win.exec_()
        else:
            video_win = VideoWin(self)
            video_win.exec_()

    # 清空重置界面1数据
    def reset1(self):
        self.identify_record = []
        self.date_show.setText("--")
        self.identify_record_path = ""

    # ========== 用户管理相关函数 =============
    # 获取所有用户
    def select_all2(self):
        op_mysql = A_sql.OperationMysql()
        self.users_list = op_mysql.search("select * from users;")

    # 显示用户数据
    def show_table2(self):
        self.table_view2.setRowCount(len(self.users_list))  # 行
        for i in range(len(self.users_list)):
            checkbox = QCheckBox()
            checkbox.setStyleSheet("padding-left:5px;")
            self.table_view2.setCellWidget(i, 0, checkbox)
            self.table_data(self.table_view2, i, 0, self.users_list[i]['user_id'])
            self.table_data(self.table_view2, i, 1, self.users_list[i]['user_type'])

    # 同意注册申请
    def agree_user(self):
        select_list = []
        for i in range(self.table_view2.rowCount()):
            item = self.table_view2.cellWidget(i, 0)
            if item.isChecked():
                select_list.append(self.users_list[i])
        if len(select_list) == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("请先选择用户账号信息！")
            msg_box.exec_()
        else:
            for i in select_list:
                op_mysql = A_sql.OperationMysql()
                op_mysql.update_one(
                    "update users set user_type='已通过' where (user_id=  '" + str(i['user_id']) + "')")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("操作成功！")
            msg_box.exec_()
        self.select_all2()
        self.show_table2()

    # 注销账号
    def delete_user(self):
        select_list = []
        for i in range(self.table_view2.rowCount()):
            item = self.table_view2.cellWidget(i, 0)
            if item.isChecked():
                select_list.append(self.users_list[i])
        if len(select_list) == 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("请先选择要注销的用户账号！")
            msg_box.exec_()
        else:
            reply = QMessageBox.question(None, '确认', '你确定要执行这个操作吗？', QMessageBox.Yes | QMessageBox.No)
            # 处理用户的回答
            if reply == QMessageBox.Yes:
                for i in select_list:
                    # 删除该账号对应的所有记录
                    op_mysql = A_sql.OperationMysql()
                    identify_record = op_mysql.search(
                        "select * from records where record_user_id = '" + i['user_id'] + "';")
                    for j in identify_record:
                        if j['record_name'][0:1] == 'v':
                            os.remove("./A_output/videos/" + j['record_name'])
                        elif j['record_name'][0:1] == 'c':
                            os.remove("./A_output/camera/" + j['record_name'])
                        elif j['record_name'][0:1] == 'i':
                            os.remove("./A_output/images/" + j['record_name'])
                        op_mysql = A_sql.OperationMysql()
                        op_mysql.delete_one("delete from records where record_id= '" + str(j['record_id']) + "'")
                    # 删除账号信息
                    op_mysql = A_sql.OperationMysql()
                    op_mysql.delete_one("delete from users where user_id='" + i['user_id'] + "';")
                # 创建一个消息框
                msg_box = QMessageBox()
                msg_box.setWindowTitle("提示")
                msg_box.setText("注销成功，对应记录已全部删除，程序退出!")
                # 显示消息框
                msg_box.exec_()
        self.select_all2()
        self.show_table2()

    # ========== 账号管理相关函数 =============
    def show_admin(self):
        if len(self.admin_list) != 0:
            self.admin_id2.setText(self.admin_list[0])
            self.admin_pwd2.setText(self.admin_list[1])

    def upd_password(self):
        if len(self.admin_pwd2.text()) != 0:
            if self.admin_pwd2.text() != self.admin_list[1]:
                self.admin_list[1] = self.admin_pwd2.text()
                op_mysql = A_sql.OperationMysql()
                op_mysql.update_one(
                    "update admin set admin_pwd='" + self.admin_list[1] + "' where (admin_id=  '" + self.admin_list[
                        0] + "')")
                # 创建一个消息框
                msg_box = QMessageBox()
                msg_box.setWindowTitle("提示")
                msg_box.setText("修改成功!")
                # 显示消息框
                msg_box.exec_()
            else:
                # 创建一个消息框
                msg_box = QMessageBox()
                msg_box.setWindowTitle("提示")
                msg_box.setText("密码与原密码一致!")
                # 显示消息框
                msg_box.exec_()
        else:
            # 创建一个消息框
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("请先输入账号信息!")
            # 显示消息框
            msg_box.exec_()


# 日期选择界面类
class DateWin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日期查询")
        self.selected_date = ""
        self.calendar = QCalendarWidget()
        self.button = QPushButton('选择日期')
        self.button.clicked.connect(self.accept)
        # 创建布局并添加部件
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.button)
        self.setLayout(layout)


# 查看图像界面类
class ImageWin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像")
        self.resize(1000, 600)
        self.show = QLabel(self)
        self.show.setText("")
        self.show.setFixedSize(900, 500)
        self.show.move(50, 50)
        self.show.setAlignment(Qt.AlignCenter)
        self.show.setStyleSheet("QLabel{border: 2px solid gray;font-size:30px;font-family:'黑体';color:#999999;}")
        input_image = cv2.imread(parent.identify_record_path)
        show_input_img = self.change_image(input_image, 900, 500)
        # 将检测图像画面显示在界面
        show_input_img = cv2.cvtColor(show_input_img, cv2.COLOR_BGR2RGB)
        show_input_img = QImage(show_input_img.data, show_input_img.shape[1], show_input_img.shape[0],
                                show_input_img.shape[1] * 3, QImage.Format_RGB888)
        self.show.setPixmap(QPixmap.fromImage(show_input_img))

    # 改变图像大小在界面显示
    @staticmethod
    def change_image(input_image, width, height):
        if input_image is not None:
            # 更换为界面适应性大小显示
            wh = float(int(input_image.shape[1]) / int(input_image.shape[0]))
            show_wh = width / height
            if int(input_image.shape[1]) > height or int(input_image.shape[0]) > width:
                if show_wh - wh < 0:
                    w = width
                    h = int(w / wh)
                    output_image = cv2.resize(input_image, (w, h))
                else:
                    h = height
                    w = int(h * wh)
                    output_image = cv2.resize(input_image, (w, h))
            else:
                output_image = input_image
            return output_image
        else:
            return input_image


class VideoWin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cap = cv2.VideoCapture()
        self.timer_video = QTimer()
        self.timer_video.timeout.connect(self.show_video)
        self.path = parent.identify_record_path
        self.setWindowTitle("视频")
        self.resize(1000, 600)
        self.show = QLabel(self)
        self.show.setText("显示区")
        self.show.setFixedSize(900, 500)
        self.show.move(50, 20)
        self.show.setAlignment(Qt.AlignCenter)
        self.show.setStyleSheet("QLabel{border: 2px solid gray;font-size:30px;font-family:'黑体';color:#999999;}")
        self.play_button = QPushButton(self)
        self.play_button.setFixedSize(440, 50)
        self.play_button.move(50, 530)
        self.play_button.setText("播放")
        self.play_button.clicked.connect(self.play)
        self.play_button.setStyleSheet("QPushButton{background:#ffffff;color:#999999;font-weight:600;"
                                       "font-size:18px;font-family:'黑体';border: 2px solid gray;}"
                                       "QPushButton:hover{background:#e6e6e6;}")
        self.stop_button = QPushButton(self)
        self.stop_button.setText("关闭")
        self.stop_button.setFixedSize(440, 50)
        self.stop_button.move(510, 530)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setStyleSheet("QPushButton{background:#ffffff;color:#999999;font-weight:600;"
                                       "font-size:18px;font-family:'黑体';border: 2px solid gray;}"
                                       "QPushButton:hover{background:#e6e6e6;}")

    def play(self):
        if not self.timer_video.isActive():
            self.cap.open(self.path)
            self.timer_video.start(30)

    def stop(self):
        self.timer_video.stop()
        self.show.clear()
        self.show.setText("显示区")

    def show_video(self):
        flag, image = self.cap.read()
        if image is not None:
            show_input_img = self.change_image(image, 900, 500)
            # 将检测图像画面显示在界面
            show_input_img = cv2.cvtColor(show_input_img, cv2.COLOR_BGR2RGB)
            show_input_img = QImage(show_input_img.data, show_input_img.shape[1], show_input_img.shape[0],
                                    show_input_img.shape[1] * 3, QImage.Format_RGB888)
            self.show.setPixmap(QPixmap.fromImage(show_input_img))
        else:
            self.stop()

    # 改变图像大小在界面显示
    @staticmethod
    def change_image(input_image, width, height):
        if input_image is not None:
            # 更换为界面适应性大小显示
            wh = float(int(input_image.shape[1]) / int(input_image.shape[0]))
            show_wh = width / height
            if int(input_image.shape[1]) > height or int(input_image.shape[0]) > width:
                if show_wh - wh < 0:
                    w = width
                    h = int(w / wh)
                    output_image = cv2.resize(input_image, (w, h))
                else:
                    h = height
                    w = int(h * wh)
                    output_image = cv2.resize(input_image, (w, h))
            else:
                output_image = input_image
            return output_image
        else:
            return input_image

    def closeEvent(self, event):
        # 在窗口关闭时执行的操作
        self.stop()
        event.accept()