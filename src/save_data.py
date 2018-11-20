import pickle


class GraphData(object):

    def __init__(self, sale):
        self.sale_list = []
        self.add(sale)

    def add(self, sale):
        self.sale_list.append(sale)


class SaveItem(object):

    def __init__(self, week_sale, today_graph):
        self.week_sales = week_sale
        self.today_graph_data = today_graph

    def add(self, sale):
        new_data = GraphData(sale)
        self.today_graph_data.insert(0, new_data)
        self.week_sales.insert(0, new_data)


class SaveData(object):

    day_itr = 0
    hour_itr = 0

    def __init__(self):
        self.save_items = {}

    def add_sale(self, item_id_str, sale_data):
        if item_id_str in self.save_items:
            self.save_items[item_id_str].add(sale_data)
        else:
            self.save_items[item_id_str] = SaveItem(week_sale=[sale_data], today_graph=[sale_data])

    def save(self, file):
        with open(file, mode='wb') as f:
            pickle.dump(self.save_items, f)

    def load(self, file):
        with open(file, mode='rb') as f:
            self.save_items = pickle.load(f)
