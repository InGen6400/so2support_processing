from src import sale_data
from src import save_data


class SendItem(object):

    cheapest_now: sale_data.SaleData
    cheap5_week_ave: float
    cheap5_day_ave: float

    def __init__(self, cheap5_day_ave=0, cheap5_week_ave=0, cheapest_now=None):
        """
        :param float cheap5_day_ave:
        :param float cheap5_week_ave:
        :param sale_data.SaleData cheapest_now:
        """
        self.cheap5_day_ave = cheap5_day_ave
        self.cheap5_week_ave = cheap5_week_ave
        self.cheapest_now = cheapest_now

    def load(self, week_sale_list):
        """
        :param list[list[sale_data.SaleList]] week_sale_list:
        :return:
        """
        sum_num = 0
        sum_weighted_price = 0
        # 日付についてループ
        for day_delta in range(0, len(week_sale_list)):
            if week_sale_list[day_delta]:
                # 時刻についてループ
                for hour in range(0, len(week_sale_list[day_delta])):
                    sum_num = sum_num + week_sale_list[day_delta][hour].sum_num()
                    sum_weighted_price = week_sale_list[day_delta][hour].sum_weighted_price()
                    # 今日の直近の時間
                    if day_delta == 0 and hour == 0:
                        self.cheapest_now = week_sale_list[day_delta][hour].get_cheapest()
                # 今日のデータ
                if day_delta == 0:
                    self.cheap5_day_ave = sum_weighted_price / sum_num
        self.cheap5_week_ave = sum_weighted_price / sum_num

    def to_dict(self):
        dst = {
            u'cheap5_day_ave': self.cheap5_day_ave,
            u'cheap5_week_ave': self.cheap5_week_ave,
            u'cheapest_now': self.cheapest_now
        }
        return dst


class SendData(object):

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
