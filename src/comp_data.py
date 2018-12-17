from typing import List

from src.sale_data import SaleList


class CompSaleList:

    def __init__(self, today_sale: List[List[SaleList]]):
        self.sum_weighted_price = 0
        self.sum_num = 0
        for one_hour in today_sale:
            for dars in one_hour:
                self.sum_num = self.sum_num + dars.sum5_num()
                self.sum_weighted_price = self.sum_weighted_price + dars.sum5_weighted_price()

    def to_dict(self):
        """
        :rtype: dict
        """
        return {
            u'price': self.sum_weighted_price,
            u'num': self.sum_num
        }

