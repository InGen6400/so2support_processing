from typing import Dict, List

from src import sale_data
from src import save_data


class SendItem(object):

    cheapest_now: List[sale_data.SaleData]
    cheap5_week_ave: float
    cheap5_day_ave: float

    def __init__(self, cheap5_day_ave=0, cheap5_week_ave=0, cheapest_now=None):
        """
        :param float cheap5_day_ave:
        :param float cheap5_week_ave:
        :param list[sale_data.SaleData] cheapest_now:
        """
        self.cheap5_day_ave = cheap5_day_ave
        self.cheap5_week_ave = cheap5_week_ave
        self.cheapest_now = cheapest_now

    def load(self, week_sale_list):
        """
        :param list[list[list[sale_data.SaleList]]] week_sale_list:
        :return:
        """
        sum_num = 0
        sum_weighted_price = 0
        # 日付についてループ
        for day_delta in range(0, len(week_sale_list)):
            if week_sale_list[day_delta]:
                day_sum_num = 0
                day_sum_price = 0
                # 時刻についてループ
                for hour in range(0, len(week_sale_list[day_delta])):
                    # 12分区切りについてループ
                    for dars in range(0, len(week_sale_list[day_delta][hour])):
                        day_sum_num = day_sum_num + week_sale_list[day_delta][hour][dars].sum5_num()
                        day_sum_price = day_sum_price + week_sale_list[day_delta][hour][dars]\
                            .sum5_weighted_price()
                        # 今日の直近の時間
                        if day_delta == 0 and hour == 0 and dars == 0:
                            self.cheapest_now = week_sale_list[day_delta][hour][dars].get_cheapest()
                sum_num = sum_num + day_sum_num
                sum_weighted_price = sum_weighted_price + day_sum_price
                # 昨日のデータ
                if day_delta == 1:
                    self.cheap5_day_ave = day_sum_price / day_sum_num
        self.cheap5_week_ave = sum_weighted_price / sum_num

    def to_dict(self):
        cheapest_now = []
        for cheapest in self.cheapest_now:
            cheapest_now.append(cheapest.to_dict())
        dst = {
            u'cheap5_day_ave': self.cheap5_day_ave,
            u'cheap5_week_ave': self.cheap5_week_ave,
            u'cheapest_now': cheapest_now
        }
        return dst


class SendData(object):

    send_items: Dict[str, SendItem]

    def __init__(self):
        self.send_items = {}

    def load(self, save: save_data.SaveData):
        """
        :param SaveData save:
        """
        # 全アイテムについてのループ
        for key, item in save.save_items.items():
            send_item = SendItem()
            send_item.load(save.save_items[key].week_sale_lists)
            self.send_items[key] = send_item

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
