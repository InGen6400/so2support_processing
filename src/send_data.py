
from src import sale_data


class SendItem(object):

    def __init__(self):
        self.cheap5_day = []
        self.cheap5_week = []
        self.ave_3day = -1
        self.cheapest = sale_data.SaleData()

    def to_dict(self):
        dest = {
            u'cheap5_day': self.cheap5_day,
            u'cheap5_week': self.cheap5_week,
            u'ave3': self.ave_3day,
            u'cheapest': self.cheapest
        }
        return dest


class SendData(object):

    def __init__(self):
        self.send_items = {}

    def to_dict(self):
        ret_dict = {}
        for key, item in self.send_items.items():
            ret_dict[key] = item.to_dict()
        return ret_dict
