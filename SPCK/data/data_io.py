import json

def load_json_data(file_json):
    """
    Đọc dữ liệu (READ)
    """
    item_dict_data = []
    with open(file_json, "r",encoding='utf-8') as json_in:
        json_data = json.load(json_in)
    item_dict_data.extend(json_data)
    return item_dict_data

def write_json_data(json_data, file_json):
    """
    Viết dữ liệu (WRITE)
    """
    with open (file_json, "w",encoding='utf-8') as json_out:
        json.dump(json_data, json_out,ensure_ascii=False, indent = -4)