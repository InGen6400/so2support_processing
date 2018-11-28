import pickle
import datetime
import os
from datetime import datetime
from typing import List, Dict, Any

from src import sale_data
from src.sale_data import SaleList

save_dir = 'save'
graph_dir = 'save/graph'
graph_file_name = 'graph'
n_sale_1day = 24*5


class GraphData(object):

    def __init__(self, ave, hour):
        self.ave_price = ave
        self.hour = hour

    def __repr__(self):
        return 'GraphData: ave:{} hour:{}'.format(self.ave_price, self.hour)


class SaveItem(object):

    today_graph: List[GraphData]
    week_sale_lists: List[List[SaleList]]

    def __init__(self, sale):
        # week_sales[7*120]
        self.week_sale_lists = [[sale_data.SaleList(sale)]]
        # today_graph[<24]
        self.today_graph = []

    # データの追加
    def add(self, sale):
        self.week_sale_lists[0][0].add(sale)

    # 日付が変わったらグラフデータをファイルに出力
    def change_day(self, old):
        day_str = str(old)
        with open(os.path.join(graph_dir, graph_file_name + day_str + '.pkl'), mode='wb') as f:
            pickle.dump(self.today_graph, f)
        self.today_graph = []
        self.week_sale_lists.insert(0, [])
        self.week_sale_lists = self.week_sale_lists[:7]

    # 時間が変わったら一時間の平均を今日のグラフデータに追加して一時間のデータを消す
    def change_hour(self, old):
        sale_list = self.week_sale_lists[0][0]
        if sale_list:
            self.today_graph.append(GraphData(sale_list.sum_price() / sale_list.sum_num(), old))

    def __repr__(self):
        return 'SaveItem \n \tweek_sales:{} \n \ttoday_graph:{}'.format(self.week_sale_lists, self.today_graph)


class SaveData(object):

    hour: int
    day: int
    save_items: Dict[str, SaveItem]

    def __init__(self, day=datetime.today().day, hour=datetime.today().hour):
        self.save_items = {}
        self.day = day
        self.hour = hour
        self.mod_time = datetime.datetime.today()
        if os.path.exists(os.path.join(save_dir, 'save_data.pkl')) & \
                os.path.exists(os.path.join(save_dir, 'time_data.pkl')):
            self.load()

    def on_change_day(self, old):
        for item in self.save_items.values():
            item.change_day(old)

    def on_change_hour(self, old):
        for item in self.save_items.values():
            item.change_hour(old)

    def add_sale(self, item_id_str, sale):
        # すでに同じIDのアイテムがあるなら追加，ないなら新規作成
        if item_id_str in self.save_items:
            self.save_items[item_id_str].add(sale)
        else:
            self.save_items[item_id_str] = \
                SaveItem(sale)

    def load_json(self, json_dict):
        """
        :type json_dict: dict
        :rtype: int
        """

        # 日付が変わった
        if self.day != datetime.date.today().day:
            self.on_change_day(self.day)
            self.day = datetime.date.today().day

        # 時間が変わった
        if self.hour != datetime.datetime.today().hour:
            self.on_change_hour(self.hour)
            self.hour = datetime.datetime.today().hour

        n_loaded = 0
        for one_data in json_dict:
            if one_data['item_id'] < 5000:
                data = sale_data.SaleData(one_data['price'], one_data['unit'], one_data['area_id'], one_data['pos_x'],
                                          one_data['pos_y'], one_data['bundle_sale'], one_data['user_id'])
                self.add_sale(str(one_data['item_id']), data)
                n_loaded = n_loaded + 1

        return n_loaded

    def save_time(self):
        with open(os.path.join(save_dir, 'time_data.pkl'), mode='wb') as f:
            pickle.dump(self.day, f)
            pickle.dump(self.hour, f)

    def save(self):
        with open(os.path.join(save_dir, 'save_data.pkl'), mode='wb') as f:
            pickle.dump(self.save_items, f)
        self.save_time()

    def load(self):
        with open(os.path.join(save_dir, 'save_data.pkl'), mode='rb') as f:
            self.save_items = pickle.load(f)
        with open(os.path.join(save_dir, 'time_data.pkl'), mode='rb') as f:
            self.day = pickle.load(f)
            self.hour = pickle.load(f)
