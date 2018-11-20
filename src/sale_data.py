
class SaleData(object)  :

    def __init__(self, price, pos_x, pos_y, area_id, num, bundle, user):
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
            u'bundle': self.bundle,
            u'user': self.user
        }
        return ret

    def __repr__(self):
        return u'SaleData(price: {})'.format(self.price)


class SaleList(object):

    def __init__(self, in_data):
        self.sale_data = []
        self.add(in_data)

    def add(self, in_data):
        self.sale_data.append(in_data)

    def add_individual(self, price, pos_x, pos_y, area_id, unit):
        self.sale_data.append(SaleData(price, pos_x, pos_y, area_id, unit))

    def sum_num(self):
        num = 0
        for data in self.sale_data:
            num = num + data.num
        return num

    def sum_price(self):
        price = 0
        for data in self.sale_data:
            price = price + data.price
        return price

    # 最低，最大価格．平均，トップ5を計算する．
    def calc(self):
        self.sale_data = sorted(self.sale_data, key=lambda u: u.price)
        min_price = self.sale_data[0].price
        max_price = self.sale_data[-1].price
        ave = self.sum_price()/self.sum_num()
        # 最大で5つ，配列の長さが5以下なら配列の長さ
        top5 = self.sale_data[:min(len(self.sale_data), 5)]
        return min_price, max_price, ave, top5

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
