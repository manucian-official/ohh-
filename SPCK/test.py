import sys
import webbrowser

from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

from models.model import ItemList
from data import data_io
from widget.dialog import AddDialog, EditDialog, ManagerCheckDialog

class ProductCard(QWidget):
    def __init__(self, item, main):
        super().__init__()
        self.item = item
        self.ui = uic.loadUi("ui/product_card.ui", self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.main = main

        self.ui.btn_delete.setEnabled(False)
        if main.current_user and main.current_user["status"] == "manager":
            self.ui.btn_delete.setEnabled(True)

        pixmap = QPixmap(item.image)
        scaled = pixmap.scaled(self.ui.label_image.size(),
                                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                Qt.TransformationMode.SmoothTransformation
                                )
        self.ui.label_image.setPixmap(scaled)
        self.ui.label_name.setText(item.title)

        self.ui.label_price.setText(f"{item.price:,}đ")

        self.ui.btn_delete.clicked.connect(self.delete_item)
        self.ui.btn_add_to_bag.clicked.connect(self.add_to_bag)
        self.msg_box = QMessageBox()

    def delete_item(self):
        self.msg_box.setText(f"Bạn có chắc muốn xóa sản phẩm {self.item.title}?")
        self.msg_box.setIcon(QMessageBox.Icon.Question)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if self.msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.main.item.delete_item(self.item.title)
            self.main.load_shop_item() #Load lại shop item sau khi xóa

    def mousePressEvent(self, event):
        self.main.card_clicked(self)

    def add_to_bag(self):
        self.msg_box.setText(f"Bạn có muốn thêm sản phẩm {self.item.title} vào giỏ hàng?")
        self.msg_box.setIcon(QMessageBox.Icon.Question)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if self.msg_box.exec() == QMessageBox.StandardButton.Yes:
            new_item = self.item.__dict__.copy()
            if new_item["stock"] <= 0:
                self.msg_box.setText(f"Sản phẩm {self.item.title} đã hết hàng!")
                self.msg_box.setIcon(QMessageBox.Icon.Warning)
                self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                self.msg_box.exec()
                return
            new_item["quantity"] = 1
            new_item["stock"] -= 1
            self.main.item.edit_item(self.item.title, new_item)
            for i in self.main.bag_item:
                if self.item.title == i["title"]:
                    i["quantity"] += 1
                    i["stock"] -= 1
                    self.main.item.edit_item(self.item.title, i)
                    self.main.item.edit_item
                    self.main.load_data_table()
                    return
            self.main.bag_item.append(new_item)
            self.main.load_data_table()

class User:
    def __init__(self, fname, sname, email, password, status = None):
        self.fname = fname
        self.sname = sname
        self.email = email
        self.password = password
        self.status = status

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/register.ui", self)
        self.infor_dict_data = data_io.load_json_data("data/data.json")
        # sự kiện:
        self.ui.btn_back.clicked.connect(self.back_login)
        self.ui.btn_signup.clicked.connect(self.check_signup)
        self.msg_box = QMessageBox()
        self.current_user = None

    def check_signup(self):
        fname = self.ui.lineEditFName.text()
        sname = self.ui.lineEditSName.text()
        email = self.ui.lineEditEmail.text()
        password = self.ui.lineEditPassword.text()
        check_password = self.ui.lineEditcheckPassword.text()

        if len(fname) == 0 or len(sname) == 0 or len(email) == 0 or len(password) == 0 or len(check_password) == 0:
            self.msg_box.setText("Vui lòng nhập đầy đủ thông tin đăng kí")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()
        else:
            if password == check_password:
                self.msg_box.setText(f"Chào mừng thành viên mới đến với MUIC, {fname} {sname}")
                self.msg_box.setIcon(QMessageBox.Icon.Information)
                self.msg_box.exec()
                new_acc = User(fname,sname,email,password, status = "user")
                self.close()
                main.show()
                # lưu vào json
                self.infor_dict_data.append(new_acc.__dict__)
                data_io.write_json_data(self.infor_dict_data, "data/data.json")
                # lưu người dùng mới thành người dùng hiện tại
                self.current_user = self.infor_dict_data[-1]
                main.current_user = self.current_user
                main.check_user()
            else:
                self.msg_box.setText("Mật khẩu không trùng khớp")
                self.msg_box.setIcon(QMessageBox.Icon.Critical)
                self.msg_box.exec()

    def back_login(self):
        self.close()
        login.show()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/log_in.ui", self)
        self.infor_dict_data = data_io.load_json_data("data/data.json")
        # sự kiện
        self.ui.btn_c_acc.clicked.connect(self.go_to_register)
        self.ui.btn_forget.clicked.connect(self.forget_password)
        self.ui.btn_login.clicked.connect(self.go_to_main)
        self.msg_box = QMessageBox()

    def go_to_main(self):
        email = self.ui.lineEditEmail.text()
        password = self.ui.lineEditPassword.text()
        if len(email) == 0 or len(password) == 0:
            self.msg_box.setText("Vui lòng nhập đầy đủ thông tin đăng kí")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()
        else:
            for acc in self.infor_dict_data:
                if email == acc["email"] and password == acc["password"]:
                    self.msg_box.setText("Chào mừng quay trở lại, Manucian!")
                    self.msg_box.setIcon(QMessageBox.Icon.Information)
                    self.msg_box.exec()
                    acc["status"] = "user"
                    main.current_user = acc #Lưu người dùng hiện tại
                    main.check_user()
                    self.close()
                    main.show()
                    return
                
            self.msg_box.setText("Email hoặc Password không trùng khớp")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()

    def forget_password(self):
        self.close()
        forget1.show()

    def go_to_register(self):
        self.close()
        register.show()
          
class Forget1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/forget1.ui", self)
        self.ui.btn_confirm.clicked.connect(self.next)
        self.ui.btn_back.clicked.connect(self.back)
        self.msg_box = QMessageBox()

    def next(self):
        fname = self.ui.lineEditFName.text()
        sname = self.ui.lineEditSName.text()
        email = self.ui.lineEditEmail.text()
        if len(fname) == 0 or len(sname) == 0 or len(email) == 0:
            self.msg_box.setText("Vui lòng nhập đầy đủ thông tin đăng kí")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()
        else:
            for acc in register.infor_dict_data:
                if email == acc["email"] and fname == acc["fname"] and sname == acc["sname"]:
                    self.msg_box.setText("Hoàn thành!")
                    self.msg_box.setIcon(QMessageBox.Icon.Information)
                    self.msg_box.exec()
                    forget1.close()
                    forget2.show()
                    return
            self.msg_box.setText("Email hoặc First Name hoặc Surname không trùng khớp")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()

    def back(self):
        self.close()
        login.show()

class Forget2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/forget2.ui", self)
        self.ui.btn_confirm.clicked.connect(self.confirm)
        self.ui.btn_back.clicked.connect(self.back)
        self.msg_box = QMessageBox()

    def confirm(self):
        password = self.ui.lineEditPassword.text()
        check_password = self.ui.lineEditcheckPassword.text()

        if len(password) == 0 or len(check_password) == 0:
            self.msg_box.setText("Vui lòng nhập đầy đủ thông tin đăng kí")
            self.msg_box.setIcon(QMessageBox.Icon.Critical)
            self.msg_box.exec()
        else:
            if password == check_password:
                self.msg_box.setText(f"Chào mừng quay trở lại, Manucian!")
                self.msg_box.setIcon(QMessageBox.Icon.Information)
                self.msg_box.exec()
                for acc in register.infor_dict_data:
                    if forget1.ui.lineEditFName.text() == acc["fname"] and forget1.ui.lineEditSName.text() == acc["sname"] and forget1.ui.lineEditEmail.text() == acc["email"]:
                        acc["password"] = password
                        data_io.write_json_data(register.infor_dict_data, "data/data.json")
                self.close()
                main.show()
    
    def back(self):
        self.close()
        login.show()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/home.ui", self)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.shop_layout = self.ui.scrollAreaWidgetContents.layout()

        self.bag_item = []

        self.item = ItemList()
        self.item.load_data()

        self.load_data_table()

        self.selected_card = None
        self.msg_box = QMessageBox()

        self.current_user = None

        self.ui.btn_edit.setEnabled(False)

    def check_user(self):
        if self.current_user:
            self.ui.label_status.setText(f"{self.current_user["status"]}" if self.current_user else "No user")
            self.ui.label_username.setText(f"{self.current_user["fname"]} {self.current_user["sname"]}" if self.current_user else "No user")

        # sự kiện
        """
        Main Page
        """
        self.ui.btn_shop.clicked.connect(self.go_to_shop)
        self.ui.btn_home.clicked.connect(self.go_to_home)
        self.ui.btn_bag.clicked.connect(self.go_to_bag)
        self.ui.btn_history.clicked.connect(self.go_to_history)
        self.ui.btn_infor.clicked.connect(self.go_to_infor)
        self.ui.btn_user.clicked.connect(self.go_to_user)
        # URL
        self.ui.btn_fulham.clicked.connect(self.fulham_url)
        self.ui.btn_everton.clicked.connect(self.everton_url)
        self.ui.btn_westham.clicked.connect(self.westham_url)
        self.ui.btn_tot.clicked.connect(self.tot_url)
        """
        CRUD Page
        """
        self.ui.btn_add.clicked.connect(self.add)
        self.ui.btn_edit.clicked.connect(self.edit)
        self.ui.lineEdit_search.textChanged.connect(self.search)
        """
        Bag
        """
        self.ui.btn_pay.clicked.connect(self.pay)
        """
        User
        """
        self.ui.btn_man.clicked.connect(self.go_to_managerCheck)

    def load_shop_item(self):
        self.selected_card = None
        column = 3

        while self.shop_layout.count():
            child = self.shop_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for index, item in enumerate(self.item.item_list):
            row = index//column #hàng
            col = index%column #cột

            widget = ProductCard(item,self)
            widget.ui.setMinimumSize(200,350)
            self.shop_layout.addWidget(widget, row, col)

    def card_clicked(self, card):
        if self.selected_card:
            self.selected_card.setStyleSheet("") #reset lại style cho card đã chọn trước đó
            
        self.selected_card = card
        self.selected_card.setStyleSheet("border: 2px solid red;") #đổi style cho card được chọn

    # CRUD
    def add(self):
        add_dialog = AddDialog()
        if add_dialog.exec():
            new_product = add_dialog.input_fields() #trả về dict
            if new_product["title"] == "" or new_product["price"] == "" or new_product["category"] == "" or new_product["size"] == "" or new_product["stock"] == 0:
                self.msg_box.setText("Vui lòng nhập đầy đủ thông tin sản phẩm")
                self.msg_box.setIcon(QMessageBox.Icon.Critical)
                self.msg_box.exec()
                self.add()
            else:
                self.item.add_item(new_product)# thêm vào danh sách đối tượng và lưu vào json
                self.load_shop_item() #Load lại shop item sau khi thêm mới
                self.load_data_table() #Load lại data table sau khi thêm mới

    def edit(self):
        if self.selected_card is not None:
            edit_dialog = EditDialog(self.selected_card.item)
            if edit_dialog.exec():
                edited_product = edit_dialog.return_input_fields()
                if edited_product["title"] == "" or edited_product["price"] == "" or edited_product["category"] == "" or edited_product["size"] == "" or edited_product["stock"] == 0:
                    self.msg_box.setText("Vui lòng nhập đầy đủ thông tin sản phẩm")
                    self.msg_box.setIcon(QMessageBox.Icon.Critical)
                    self.msg_box.exec()
                    self.edit()
                else:
                    self.item.edit_item(self.selected_card.item.title, edited_product)
                    self.load_shop_item() #Load lại shop item sau khi sửa đổi
                    self.load_data_table() #Load lại data table sau khi sửa đổi
        else:
            self.msg_box.setText("Vui lòng chọn một sản phẩm để sửa đổi")
            self.msg_box.setIcon(QMessageBox.Icon.Warning)
            self.msg_box.exec()

    def search(self):
        search_text = self.ui.lineEdit_search.text().lower()
        matched_items = self.item.search_by_title(search_text)
        # Xử lý các sản phẩm phù hợp (ví dụ: hiển thị lại trong giao diện)
        self.selected_card = None
        column = 3
        while self.shop_layout.count():
            child = self.shop_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for index, item in enumerate(matched_items):
            row = index//column #hàng
            col = index % column #cột

            widget = ProductCard(item,self)
            widget.ui.setMinimumSize(200, 350)
            self.shop_layout.addWidget(widget, row, col)

    # BAG
    def load_data_table(self):
        total = 0
        data = self.bag_item
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(9)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Title", "Price", "Category", "Size", "Quantity", "Image", "Description", "Item Total", ""])

        for row, item in enumerate(data):
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(item["title"]))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(f"{item["price"]:,}đ"))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(item["category"]))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(item["size"]))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(item["quantity"])))
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(item["image"]))
            self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(item["description"]))
            etotal = item["price"] * item["quantity"]
            self.ui.tableWidget.setItem(row, 7, QTableWidgetItem(f"{etotal:,}đ"))
            btn = QPushButton("Xóa")
            btn.setStyleSheet("""
                QPushButton {
                              background-color:red;
                              color: white;
                              font: bold 11pt "Segoe UI";
                              border-radius: 10px;
                              border: none;
                              padding: 8px 20px;
                            }
                              """)
            
            btn.clicked.connect(self.delete)
            self.ui.tableWidget.setCellWidget(row, 8, btn)
            # Hiện total
            total += etotal
            self.ui.lineEdit_total.setText(f"{total:,}đ")
        
    def delete(self):
        self.msg_box.setText("Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?")
        self.msg_box.setIcon(QMessageBox.Icon.Question)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if self.msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.bag_item.pop(self.ui.tableWidget.currentRow())
            self.load_data_table()
            self.ui.lineEdit_total.setText("0đ")

    def pay(self):
        self.msg_box.setText("Bạn có chắc muốn thanh toán giỏ hàng không?")
        self.msg_box.setIcon(QMessageBox.Icon.Question)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if self.msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.bag_item.clear()
            self.load_data_table()
            self.msg_box.setText("Cảm ơn bạn đã mua hàng tại MUIC!")
            self.msg_box.setIcon(QMessageBox.Icon.Information)
            self.msg_box.exec()
            self.ui.lineEdit_total.setText("0đ")
    
    # Navigation

    def go_to_shop(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.load_shop_item()

    def go_to_bag(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def go_to_history(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        
    def go_to_home(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def go_to_infor(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def go_to_user(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.label_fname.setText(f"{self.current_user['fname']}")
        self.ui.label_sname.setText(f"{self.current_user['sname']}")
        self.ui.label_email.setText(f"{self.current_user['email']}")
        self.ui.label_password.setText(f"{self.current_user['password']}")
        self.ui.label_status_user.setText(f"{self.current_user['status']}")

    def go_to_managerCheck(self):
        manager_check_dialog = ManagerCheckDialog()
        man_password = "admin123"
        if manager_check_dialog.exec():
            if manager_check_dialog.lineEdit_passwordMan.text() == 0:
                self.msg_box.setText("Vui lòng nhập mật khẩu để xác minh tư cách quản lí")
                self.msg_box.setIcon(QMessageBox.Icon.Warning)
                self.msg_box.exec()
                self.exec()
            else:
                if manager_check_dialog.lineEdit_passwordMan.text() == man_password:
                    self.msg_box.setText("Xác minh thành công, chào mừng quản lí đã quay trở lại")
                    self.msg_box.setIcon(QMessageBox.Icon.Information)
                    self.msg_box.exec()
                    self.current_user["status"] = "manager"
                    self.ui.label_status_user.setText("manager")
                    self.ui.label_status.setText("manager")
                    self.ui.btn_edit.setEnabled(True)    
                else:
                    self.msg_box.setText("Xác minh thất bại, mật khẩu không chính xác")
                    self.msg_box.setIcon(QMessageBox.Icon.Critical)
                    self.msg_box.exec()
                    self.exec()


    # URL
    def fulham_url(self):
        webbrowser.open("https://www.youtube.com/watch?v=YvoMXCyHHmg")

    def everton_url(self):
        webbrowser.open("https://www.youtube.com/watch?v=hFIgpxDIomE")

    def westham_url(self):
        webbrowser.open("https://www.youtube.com/watch?v=7dxIXoBcPHY")

    def tot_url(self):
        webbrowser.open("https://www.youtube.com/watch?v=BGqq_D-AvBk")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    register = Register()
    login = Login()
    forget1 = Forget1()
    forget2 = Forget2()
    main = Main()
    login.show()
    app.exec()