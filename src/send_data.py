from typing import Dict, List

from src import sale_data, util
from src import save_data
from src import comp_data


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

    def load(self, save: save_data.SaveItem):
        sum_num = 0
        sum_weighted_price = 0
        # 日付についてループ
        for day_delta in range(0, len(save.week_comp_list)):
            if save.week_comp_list[day_delta]:
                day_num = save.week_comp_list[day_delta].sum_num
                day_w_price = save.week_comp_list[day_delta].sum_weighted_price
                sum_num = sum_num + day_num
                sum_weighted_price = sum_weighted_price + day_w_price
                # 昨日のデータ
                if day_delta == 1:
                    if day_num != 0:
                        self.cheap5_day_ave = day_w_price / day_num
                    else:
                        self.cheap5_day_ave = 0
        if sum_num != 0:
            self.cheap5_week_ave = sum_weighted_price / sum_num
        else:
            self.cheap5_week_ave = 0
        if save.today_sales and save.today_sales[0] and save.today_sales[0][0]:
            self.cheapest_now = save.today_sales[0][0].get_cheapest()

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
            send_item.load(item)
            self.send_items[key] = send_item

    def to_dict(self, category, item_dict):
        """
        :param str category:
        :param dict[str, dict] item_dict:
        :return dict:
        """
        ret_dict = {}
        for key, item in self.send_items.items():
            if key in item_dict:
                if item_dict[key]['category'] == category:
                    ret_dict[key] = item.to_dict()
            else:
                util.file_log_e("item_dict don't have key:" + key)
        return ret_dict
