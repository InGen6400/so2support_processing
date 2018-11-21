import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src import save_data
from src import sale_data
from src import converter
from src import json_loader
import pprint
import datetime



data = save_data.SaveData()
'''
data.load()
pprint.pprint(data.save_items)
data.add_sale('1', sale_data.SaleData(10, 1, 1, 3, 1000, 0, 3326))
data.add_sale('2', sale_data.SaleData(20, 1, 1, 3, 1000, 0, 3326))
data.add_sale('1', sale_data.SaleData(30, 1, 1, 3, 1000, 0, 3326))
data.on_change_hour()
data.add_sale('4', sale_data.SaleData(60, 1, 1, 3, 1000, 0, 3326))
data.add_sale('2', sale_data.SaleData(20, 1, 1, 3, 1000, 0, 3326))
data.add_sale('2', sale_data.SaleData(10, 1, 1, 3, 1000, 0, 3326))
data.add_sale('2', sale_data.SaleData(60, 1, 1, 3, 1000, 0, 3326))
data.add_sale('1', sale_data.SaleData(30, 1, 1, 3, 1000, 0, 3326))
data.on_change_hour()
pprint.pprint(data.save_items)
data.on_change_day()
pprint.pprint(data.save_items)
data.save()


json_dict = json_loader.load_json_file('resources/item.json')
item_list = converter.convert_item_list(json_dict)

'''
json_dict = json_loader.load_json_file('resources/all.json')
pprint.pprint(json_dict)
price_dict = converter.convert_price_list(json_dict)

'''
cred = credentials.Certificate('private/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# pprint.pprint(item_list)

doc_ref = db.collection(u'define_data').document(u'item')
doc_ref.set(item_list)

# doc_ref = db.collection(u'price_data').document(u'price')
# doc_ref.set(price_dict)

doc_ref = db.collection(u'define_data').document(u'item')
# 条件を指定して取得
fp = ['1', '2', '3']
doc = doc_ref.get(fp)
# item = item_data.ItemData.from_dict(doc.to_dict())
pprint.pprint(doc.to_dict())
'''