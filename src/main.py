import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src import JsonItemImporter as jsonImp
from src import item_data
from src import price_data
import pprint
"""
cred = credentials.Certificate('../private/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1
})
"""


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


json_dict = jsonImp.load_json_file('resources/item.json')
item_list = convert_item_list(json_dict)

json_dict = jsonImp.load_json_file('resources/all.json')
price_dict = convert_price_list(json_dict)

cred = credentials.Certificate('private/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

#pprint.pprint(item_list)

doc_ref = db.collection(u'define_data').document(u'item')
doc_ref.set(item_list)

#doc_ref = db.collection(u'price_data').document(u'price')
#doc_ref.set(price_dict)

doc_ref = db.collection(u'define_data').document(u'item')
#条件を指定して取得
fp = ['1', '2', '3']
doc = doc_ref.get(fp)
#item = item_data.ItemData.from_dict(doc.to_dict())
pprint.pprint(doc.to_dict())

