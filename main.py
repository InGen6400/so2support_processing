import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src import save_data
from src import send_data
from src import json_loader
from src import converter
import datetime
import requests
import json
import codecs
import pprint
import os
import sys
import traceback

PRICE_URL = 'https://so2-api.mutoys.com/json/sale/all.json'

data = save_data.SaveData()
sends: send_data.SendData = send_data.SendData()

# firebaseの初期化
cred = credentials.Certificate('private/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()  # type: firestore.firestore.Client

# アイテムデータの読み込み
item_list = json_loader.load_json_file('resources/item.json')
items, cats = converter.convert_item_list(item_list)
delta_time = datetime.datetime.today() - data.mod_time
# 11分以上たっていないと実行されない
if 'offline' in sys.argv or delta_time.seconds > 60*11:
    try:
        print('Accessing API & Downloading Json data....')
        if 'offline' in sys.argv:
            # デバッグ用
            price_json = json_loader.load_json_file('resources/prices.json')
            print('Json Loaded.\n')
        else:
            price_json = requests.get(PRICE_URL).json()
            print('Json Downloaded.\n')

        print('start dumping and saving...')
        # 定期保存(テスト段階では呼び出し時間を記録しておく本番では1ファイルのみ)
        with codecs.open('resources/prices.json', 'w', 'utf-8') as f:
            json.dump(price_json, f, ensure_ascii=False, indent=4)
        print('json saved.\n')

        data.save_time()
        print('time data saved\n')
        # データの読み込みと整理

        print('Save data loading...')
        data.load_json(price_json)
        print('Save data loaded\n')
        data.save()
        print('Save data saved\n')
        print('Creating send data...')
        sends.load(data)
        print('Send data created\n')
        if 'offline' not in sys.argv:
            col_ref = db.collection(u'price_data')  # type: firestore.firestore.CollectionReference
            print('sending...')
            for cat in cats:
                doc_ref = col_ref.document(cat)  # type: firestore.firestore.DocumentReference
                doc_ref.set(sends.to_dict(cat, items))
                print('Sent [' + cat + '] prices')
    except Exception as e:
        with open(os.path.join('save', 'log.txt'), 'a') as f:
            print('Error: ' + traceback.format_exc(), file=f)
        raise
    else:
        print('complete.\n')
        with open(os.path.join('save', 'log.txt'), 'a') as f:
            print('Success: ' + str(datetime.datetime.today()), file=f)
else:
    print(str(datetime.datetime.today()) + ' - ' + str(data.mod_time))
    print('delta: ' + str(delta_time))
    print('Not Enough Times')
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Failed-: ' + str(datetime.datetime.today()) + '\n\t Not Enough Times', file=f)

