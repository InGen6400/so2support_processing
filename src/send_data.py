from src import save_data
from src import item_data

class SendItem(object):

    def __init__(self, cheap5_day, cheap5_week, ave3, cheapest):
        """
        :type cheap5_day: list[dict[str, int]]
        :type cheap5_week: list[dict[str, int]]
        :type ave3: float
        :type cheapest: dict[str, int]
        """
        self.cheap5_day = cheap5_day
        self.cheap5_week = cheap5_week
        self.ave_3day = ave3
        self.cheapest = cheapest

    def to_dict(self):
        dst = {
            u'cheap5_day': self.cheap5_day,
            u'cheap5_week': self.cheap5_week,
            u'ave3': self.ave_3day,
            u'cheapest': self.cheapest
        }
        return dst


class SendData(object):

    def __init__(self):
        self.send_items = {}

    def load(self, save):
        """
        :param save_data.SaveData save:
        """
        for key, item in save.save_items.items():
            save_item = save.save_items[key]  # type: save_data.SaveItem
            sum_price = 0
            cheap5_day = []  # type: list[dict[str, int]]
            cheap5_week = []  # type: list[dict[str, int]]
            cheapest = {}  # type: dict[str, int]
            day_num = 120*1
            # 3日分のデータもしくは配列の長さ分
            ave_num = day_num*3
            for i in range(0, len(save_item.week_sales)):
                # 日別トップ5
                if i < day_num:
                    if len(cheap5_day) < 5 or save_item.week_sales[i].price < cheap5_day[-1]['price']:
                        cheap5_day.append(save_item.week_sales[i].to_dict())
                        cheap5_day.sort(key=lambda x: x['price'])
                        cheap5_day = cheap5_day[0:min(len(cheap5_day), 5)]
                # 週別トップ5
                if len(cheap5_week) < 5 or save_item.week_sales[i].price < cheap5_week[-1]['price']:
                    cheap5_week.append(save_item.week_sales[i].to_dict())
                    cheap5_week.sort(key=lambda x: x['price'])
                    cheap5_week = cheap5_week[0:min(len(cheap5_week), 5)]
                # 3日平均
                if i < ave_num:
                    sum_price = sum_price + save_item.week_sales[i]
                # 最安
                if not cheapest or save_item.week_sales[i].price < cheapest['price']:
                    cheapest = save_item.week_sales[i].to_dict()
                # 同価格なら数の多い方を選ぶ
                elif save_item.week_sales[i].price == cheapest['price'] and \
                        save_item.week_sales[i].num > cheapest['num']:
                    cheapest = save_item.week_sales[i].to_dict()
            # 3日の平均を計算
            ave3 = sum_price/ave_num
            self.send_items[key] = SendItem(cheap5_day, cheap5_week, ave3, cheapest)

    def to_dict(self, category, item_dict):
        """
        :param str category:
        :param dict[str, dict] item_dict:
        :return dict:
        """
        ret_dict = {}
        for key, item in self.send_items.items():
            if item_dict[key]['category'] == category:
                ret_dict[key] = item.to_dict()
        return ret_dict
