import operator
from datetime import datetime
from data import data_io

class Item:
    def __init__(self, title, price, category, size, stock, image, description, item_id = None):
        self.title = title
        self.price = price
        self.category = category
        self.size = size
        self.stock = stock
        self.image = image
        self.description = description 
        self.item_id = item_id
    
    def update(self, new_data:dict):
        for attribute, value in new_data.items():
            if value is not None:
                setattr(self, attribute, value)

class ItemList:
    def __init__(self):
        self.item_list = []
        self.item_dict_data = data_io.load_json_data("data/product.json")

    def load_data(self):
        """
        Phương thức chuyển đổi dữ liệu đã READ vào danh sách đối tượng
        """
        for items_dict in self.item_dict_data:
            item = Item(item_id = items_dict["item_id"],
                        title = items_dict["title"],
                        image = items_dict["image"],
                        price = items_dict["price"],
                        category= items_dict["category"],
                        size= items_dict["size"],
                        stock = items_dict["stock"],
                        description= items_dict["description"])
            self.item_list.append(item)

    def items_to_data(self):
        """
        Phương thức chuyển đổi danh sách đối tượng sang dữ liệu json
        """
        data_json = []
        for items in self.item_list:
            data_json.append(items.__dict__)
        return data_json
    
    def get_first_item_by_title(self, item_title):
        """
        Trả về đối tượng Item có title là item_title
        """
        for items in self.item_list:
            if items.title == item_title: #nếu tìm thấy (trùng tên)
                return items
        return None #không tìm thấy (không trùng tên)
    
    def add_item(self, items_dict):
        """
        Phương thức thêm một đối tượng Item mới
        """
        items_dict["item_id"] = len(self.item_list)
        new_item = Item(item_id=items_dict["item_id"],
                        title = items_dict["title"],
                        image = items_dict["image"],
                        price = items_dict["price"],
                        category= items_dict["category"],
                        size= items_dict["size"],
                        stock= items_dict["stock"],
                        description= items_dict["description"])
        self.item_list.append(new_item) #Thêm vào danh sách .py
        # Thêm vào .ui khi thêm một phần tử
        self.item_dict_data.append(items_dict)
        data_io.write_json_data(self.item_dict_data, "data/product.json")

    def edit_item(self, edit_title, new_dict):
        """
        Phương thức sửa một đối tượng Item có title là edit_title
        """
        matched = self.get_first_item_by_title(edit_title)
        if matched:
            matched.update(new_dict)
            # Thêm vào .ui mỗi khi update
            self.item_dict_data = self.items_to_data()
            data_io.write_json_data(self.item_dict_data, "data/product.json")

    def delete_item(self, delete_title):
        """
        Phương thức xoá đối tượng Item có title là delete_title
        """
        matched = self.get_first_item_by_title(delete_title)
        if matched:
            self.item_list.remove(matched)
            # Thực hiện WRITE mỗi khi thay đổi danh sách đối tượng
            self.item_dict_data = self.items_to_data()
            data_io.write_json_data(self.item_dict_data, "data/product.json")

    def search_by_title(self, search_title) -> list[Item]:
        """
        Phương thức tìm kiếm tất cả các đối tượng Item có title là search_title
        """
        matched_items = []
        for items in self.item_list:
            if search_title in items.title.lower():
                matched_items.append(items)
        return matched_items
    
    def sort_item_by_title(self):
        """
        Phương thức sắp xếp theo title 
        """
        self.item_list = sorted(self.item_list,
                                key = operator.attrgetter("title"),
                                reverse = True)
    
    def get_title_list(self):
        """
        Lấy danh sách title
        """
        return [item["title"] for item in self.item_dict_data]
        