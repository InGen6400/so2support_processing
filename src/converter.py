
from src import item_data
from src import price_data


def convert_item_list(json_data):
    ret_dict = {}
    for key, value in json_data.items():
        item = item_data.ItemData(key, value['name'], value['category'], value['scale'], value['sort'])
        ret_dict[''+key] = item.to_dict()
        if key == '20':
            return ret_dict
    return ret_dict


def convert_price_list(json_data):
    tmp_dict = {}
    ret_dict = {}
    for one_data in json_data:
        price = price_data.SaleData(one_data['price'], one_data['pos_x'], one_data['pos_y'],
                                    one_data['area_id'], one_data['unit'])
        if one_data['item_id'] < 1000000:
            if one_data['item_id'] in tmp_dict:
                tmp_dict[one_data['item_id']].add(price)
            else:
                tmp_dict[one_data['item_id']] = price_data.SaleList(price)

    for key, item in tmp_dict.items():
        ret_dict[key] = item.to_dict()

    return ret_dict
