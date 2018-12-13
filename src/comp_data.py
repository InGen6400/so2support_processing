from typing import List

from src.sale_data import SaleList


class CompSaleList:

    sum_num: int
    sum_weighted_price: int

    def __init__(self, today_sale: List[List[SaleList]]):
        self.sum_weighted_price = 0
        self.sum_num = 0
        for one_hour in today_sale:
            for dars in one_hour:
                for data in dars.sale_datas:
                    self.sum_num = self.sum_num + data.num
                    self.sum_weighted_price = self.sum_weighted_price + (data.price * data.num)

    def to_dict(self):
        """
        :rtype: dict
        """
        return {
            u'price': self.sum_weighted_price,
            u'num': self.sum_num
        }

