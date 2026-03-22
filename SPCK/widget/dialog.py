from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QPixmap, QIcon

class AddDialog(QDialog):
    """
    Hộp thoại Add
    """
    def __init__(self):
        super().__init__()
        # Load giao diện
        self.ui = uic.loadUi("ui/add_dialog.ui", self)
        # Tạo đối tượng QDir để quản lý đường dẫn
        self.dir = QDir()
        self.file_name = "" #biến lưu đường dẫn hình ảnh
        # Sự kiện
        self.ui.btn_image.clicked.connect(self.browse_files)
        self.ui.comboBox_Size.clear()
        self.ui.comboBox_Size.addItems(["S","M","L","XL","None"])

    def browse_files(self):
        """
        Phương thức mở file dialog để chọn ảnh
        """
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                    "Open file", 
                                                    "./images",
                                                    filter = "Image files (*.png *.jpg *.svg)")
        if file_name:
                pixmap = QPixmap(file_name)
                scaled = pixmap.scaled(self.ui.btn_image.size(),
                                       Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                       Qt.TransformationMode.SmoothTransformation
                )
                self.ui.btn_image.setIcon(QIcon(scaled))
                self.ui.btn_image.setIconSize(self.ui.btn_image.size())
                self.ui.btn_image.setText("") #xóa text trên button sau khi chọn ảnh
                self.ui.lineEdit_link.setText(file_name)
                self.file_name = file_name #lưu đường dẫn hình ảnh vào biến
            
    def input_fields(self) -> dict:
        """
        Thu thập dữ liệu của tất cả các trường và trả về một dict
        """
        return {
                "title": self.ui.lineEdit_Title.text(),
                "price": int(self.ui.lineEdit_Price.text().replace(",", "").replace("d", "").replace("đ", "")),
                "category": self.ui.comboBox_Category.currentText(),
                "size": self.ui.comboBox_Size.currentText(),
                "stock": int(self.ui.spinBox_stock.value()),
                "image": self.dir.relativeFilePath(self.file_name),
                "description": self.ui.textEdit.toPlainText()
            }
        
class EditDialog(QDialog):
    """
    Hộp thoại Edit
    """
    def __init__(self, item):
        super().__init__()
        # Load giao diện
        self.ui = uic.loadUi("ui/edit_dialog.ui", self)
        self.ui.comboBox_Size.clear()
        self.ui.comboBox_Size.addItems(["S","M","L","XL","None"])
        # Tạo đối tượng QDir để quản lý đường dẫn
        self.dir = QDir()
        self.file_name = item.image #biến lưu đường dẫn hình ảnh
        # Sự kiện
        self.ui.btn_image.clicked.connect(self.browse_files)
        # Điền dữ liệu của item vào các trường
        self.ui.lineEdit_Title.setText(item.title)
        self.ui.lineEdit_Price.setText(str(int(item.price)))
        self.ui.comboBox_Category.setCurrentText(item.category)
        self.ui.comboBox_Size.setCurrentText(item.size)
        self.ui.spinBox_stock.setValue(int(item.stock))
        self.ui.textEdit.setPlainText(item.description)
        pixmap = QPixmap(item.image)
        scaled = pixmap.scaled(self.ui.btn_image.size(),
                                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                Qt.TransformationMode.SmoothTransformation
                                )
        self.ui.btn_image.setIcon(QIcon(scaled))
        self.ui.btn_image.setIconSize(self.ui.btn_image.size())
        self.ui.btn_image.setText("") #xóa text trên button sau khi điền ảnh
        self.ui.lineEdit_link.setText(item.image)
    def browse_files(self):
        """
        Phương thức mở file dialog để chọn ảnh
        """
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                    "Open file", 
                                                    "./images",
                                                    filter = "Image files (*.png *.jpg *.svg)")
        if file_name:
                pixmap = QPixmap(file_name)
                scaled = pixmap.scaled(self.ui.btn_image.size(),
                                       Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                       Qt.TransformationMode.SmoothTransformation
                )
                self.ui.btn_image.setIcon(QIcon(scaled))
                self.ui.btn_image.setIconSize(self.ui.btn_image.size())
                self.file_name = file_name #lưu đường dẫn hình ảnh vào biến
            
    def return_input_fields(self) -> dict:
        """
        Thu thập dữ liệu của tất cả các trường và trả về một dict
        """
        return {
                "title": self.ui.lineEdit_Title.text(),
                "price": int(self.ui.lineEdit_Price.text().replace(",", "").replace("d", "").replace("đ", "")),
                "category": self.ui.comboBox_Category.currentText(),
                "size": self.ui.comboBox_Size.currentText(),
                "stock": int(self.ui.spinBox_stock.value()),
                "image": self.dir.relativeFilePath(self.file_name),
                "description": self.ui.textEdit.toPlainText()
                }
    
class ManagerCheckDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui/checkManager.ui", self)
                