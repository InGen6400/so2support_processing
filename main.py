import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src import save_data
from src import send_data
from src import sale_data
from src import converter
from src import json_loader
import pprint
import datetime


data = save_data.SaveData()
json_dict = json_loader.load_json_file('resources/all.json', data.mod_time)
data.load_json(json_dict)
sends = send_data.SendData()
sends.load(data)
pprint.pprint(sends.to_dict())

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