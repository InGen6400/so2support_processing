from typing import List


class SaleData:

    def __init__(self, price, num, area_id, pos_x, pos_y, bundle, user):
        self.price = price
        self.num = num
        self.area_id = area_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bundle = bundle
        self.user = user

    def __radd__(self, other):
        return other + self.price

    def to_dict(self):
        ret = {
            u'price': self.price,
            u'num': self.num,
            u'area_id': self.area_id,
            u'pos_x': self.pos_x,
            u'pos_y': self.pos_y,
            u'bundle': bool(self.bundle),
            u'user': self.user
        }
        return ret

    def __repr__(self):
        return u'SaleData(price: {} num:{})'.format(self.price, self.num)


class SaleList(object):

    sale_datas: List[SaleData]

    def __init__(self, in_data=None):
        self.sale_datas = []
        if in_data is not None:
            self.add(in_data)

    def add(self, in_data):
        self.sale_datas.append(in_data)

    def add_individual(self, price, num, area_id, pos_x, pos_y, bundle, user):
        self.sale_datas.append(SaleData(price, num, area_id, pos_x, pos_y, bundle, user))

    def sum_num(self):
        num = 0
        for data in self.sale_datas:
            num = num + data.num
        return num

    def sum_weighted_price(self):
        w_price = 0
        for data in self.sale_datas:
            w_price = w_price + (data.price * data.num)
        return w_price

    def get_cheapest(self):
        min_sale = min(self.sale_datas, key=lambda x: x.price*100000+x.num)
        min_price = min_sale.price
        return [sale for sale in self.sale_datas if sale.price == min_price]

    # 最低，最大価格．平均，トップ5を計算する．
    def calc(self):
        if self.sale_datas:
            self.sale_datas = sorted(self.sale_datas, key=lambda u: u.price)
            min_price = self.sale_datas[0].price
            if self.sale_datas.__len__() == 1:
                max_price = self.sale_datas[0].price
            else:
                max_price = self.sale_datas[-1].price
            ave = self.sum_weighted_price()/self.sum_num()
            # 最大で5つ，配列の長さが5以下なら配列の長さ
            top5 = self.sale_datas[:min(len(self.sale_datas), 5)]
            return min_price, max_price, ave, top5
        return 100000000, 0, 0, []

    def to_dict(self):
        min_price, max_price, ave, top5 = self.calc()
        top5_list = []
        for data in top5:
            top5_list.append(data.to_dict())

        ret = {
            u'min': min_price,
            u'max': max_price,
            u'ave': ave,
            u'top5': top5_list
        }
        return ret

    def __repr__(self):
        min_price, max_price, ave, top5 = self.calc()
        return u'SaleList(min:{} max:{} ave:{} top5:{})'.format(
            min_price, max_price, ave, top5)
