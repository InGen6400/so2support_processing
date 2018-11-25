import pickle
import datetime
import os
from src import sale_data

save_dir = 'save'
graph_dir = 'save/graph'
graph_file_name = 'graph'
n_sale_1day = 24*5


class GraphData(object):

    def __init__(self, ave):
        self.ave_price = ave

    def __repr__(self):
        return 'GraphData: ave:{}'.format(self.ave_price)


class SaveItem(object):

    def __init__(self, sale):
        # week_sales[7*120]
        self.week_sales = [sale]  # type: list[sale_data]
        # hour_sales[<5]
        self.hour_sales = [sale]  # type: list[sale_data]
        # today_graph[<24]
        self.today_graph = []  # type: list[GraphData]

    # データの追加
    def add(self, sale):
        self.week_sales.insert(0, sale)
        self.hour_sales.insert(0, sale)
        # 一週間分のデータのみにする
        self.week_sales = self.week_sales[:min(len(self.week_sales), 7*n_sale_1day)]
        # 1時間分のデータのみにする
        self.hour_sales = self.hour_sales[:min(len(self.week_sales), 24)]

    # 日付が変わったらグラフデータをファイルに出力
    def change_day(self):
        day_str = str(datetime.date.today() + datetime.timedelta(days=-1))
        with open(os.path.join(graph_dir, graph_file_name + day_str + '.pkl'), mode='wb') as f:
            pickle.dump(self.today_graph, f)
        self.today_graph = []

    # 時間が変わったら一時間の平均を今日のグラフデータに追加して一時間のデータを消す
    def change_hour(self):
        sum_price = 0
        if self.hour_sales:
            for hour_data in self.hour_sales:
                sum_price = sum_price + hour_data.price
            self.today_graph.append(sum_price/len(self.hour_sales))
            self.hour_sales = []

    def __repr__(self):
        return 'SaveItem: \n \tweek_sales:{} \n \ttoday_graph:{}'.format(self.week_sales, self.today_graph)


class SaveData(object):

    def __init__(self, day=datetime.datetime.today().day, hour=datetime.datetime.today().hour):
        self.save_items = {}  # type: dict[str, sale_data]
        self.day = day
        self.hour = hour
        self.mod_time = datetime.datetime.today()
        if os.path.exists(os.path.join(save_dir, 'save_data.pkl')) & \
                os.path.exists(os.path.join(save_dir, 'time_data.pkl')):
            self.load()

    def on_change_day(self):
        for item in self.save_items.values():
            item.change_day()

    def on_change_hour(self):
        for item in self.save_items.values():
            item.change_hour()

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
            self.day = datetime.date.today().day
            self.on_change_day()

        # 時間が変わった
        if self.hour != datetime.datetime.today().hour:
            self.hour = datetime.datetime.today().hour
            self.on_change_hour()

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
