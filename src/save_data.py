import pickle
import datetime
import os
import sys
from collections import deque
from typing import List, Dict, Deque

from src import sale_data, util
from src.comp_data import CompSaleList
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

    week_comp_list: Deque[CompSaleList]
    today_graph: List[GraphData]
    today_sales: List[List[SaleList]]

    def __init__(self, sale):
        # today_sales[hour][dars]
        self.today_sales = [[sale_data.SaleList(sale)]]
        # today_graph[<24]
        self.today_graph = []
        self.week_comp_list = deque(maxlen=7)

    # データの追加
    def add(self, sale):
        if not self.today_sales[-1]:
            self.new_dars(sale)
        else:
            self.today_sales[-1][-1].add(sale)

    def new_dars(self, sale=None):
        self.today_sales[-1].append(SaleList(sale))

    # 日付が変わったらグラフデータをファイルに出力
    def change_day(self, old):
        day_str = str(old)
        with open(os.path.join(graph_dir, graph_file_name + day_str + '.pkl'), mode='wb') as f:
            pickle.dump(self.today_graph, f)
        self.today_graph = []
        # 今日一日のデータを圧縮して保存
        self.week_comp_list.append(CompSaleList(self.today_sales))
        # 今日のデータをクリア
        self.today_sales.clear()
        self.today_sales = [[SaleList()]]

    # 時間が変わったら一時間の平均を今日のグラフデータに追加
    def change_hour(self, old):
        if self.today_sales:
            sale_list: List[SaleList] = self.today_sales[-1]
            sum_price = 0
            sum_num = 0
            for dars_sales in sale_list:
                sum_price = sum_price + dars_sales.sum_weighted_price()
                sum_num = sum_num + dars_sales.sum_num()
            if sum_num != 0:
                self.today_graph.append(GraphData(sum_price/sum_num, old))
            # 新しい時間の分を追加
            self.today_sales.append([SaleList()])
        else:
            util.file_log_e('no today sale')

    def __repr__(self):
        ret = 'SaveItem \n'
        ret = ret + '\ttoday_graph:\n\t\t{}\n'.format(self.today_graph)
        ret = ret+'\ttoday_sales:\n'
        for hour in range(0, len(self.today_sales)):
            for dars in range(0, len(self.today_sales[hour])):
                ret = ret + '\t\ttime ' + str(hour) + ',' + str(dars) + ': ' +\
                      self.today_sales[hour][dars].__repr__() + '\n'
        ret = ret + '\tweek_comp_list\n'
        for day in range(0, len(self.week_comp_list)):
            ret = ret + '\t\tday ' + str(day) + ': ' + str(self.week_comp_list[day].to_dict())
        return ret


class SaveData(object):

    hour: int
    day: int
    save_items: Dict[str, SaveItem]

    def __init__(self, date=datetime.datetime.today()):
        self.save_items = {}
        self.day = date.day
        self.hour = date.hour
        self.mod_time = datetime.datetime.today()
        if os.path.exists(os.path.join(save_dir, 'save_data.pkl')) & \
                os.path.exists(os.path.join(save_dir, 'time_data.pkl')):
            self.load()
        else:
            self.save()

    def on_change_day(self, old):
        for item in self.save_items.values():
            item.change_day(old)

    def on_change_hour(self, old):
        for item in self.save_items.values():
            item.change_hour(old)

    def on_change_dars(self):
        for item in self.save_items.values():
            item.new_dars()

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

        self.on_change_dars()

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
            if 'oneday' in sys.argv:
                pickle.dump(datetime.datetime.today() - datetime.timedelta(days=1), f)
            else:
                pickle.dump(datetime.datetime.today(), f)

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
            self.mod_time = pickle.load(f)
