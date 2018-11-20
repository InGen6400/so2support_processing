import pickle
import datetime

class GraphData(object):

    def __init__(self, ave):
        self.ave_price = ave


class SaveItem(object):

    def __init__(self, week_sale):
        self.week_sales = week_sale

    def add(self, sale):

        self.week_sales.insert(0, GraphData(sale))

    def change_week(self):


    def change_day(self):


    def change_hour(self):


class SaveData(object):

    save_file = ''

    def __init__(self):
        self.save_items = {}
        self.day = datetime.date.today().day
        self.hour = datetime.datetime.today().hour

    def add_sale(self, item_id_str, sale_data):
        if item_id_str in self.save_items:
            self.save_items[item_id_str].add(sale_data)
        else:
            self.save_items[item_id_str] = SaveItem(week_sale=[sale_data], today_graph=[sale_data])

        if self.day != datetime.date.today().day:
            self.day = datetime.date.today().day

        if self.hour != datetime.datetime.today().hour:
            self.hour = datetime.datetime.today().hour

    def save(self, file):
        with open(file, mode='wb') as f:
            pickle.dump(self.save_items, f)

    def load(self, file):
        with open(file, mode='rb') as f:
            self.save_items = pickle.load(f)
