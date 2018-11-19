
class SaleData:

    def __init__(self, price, pos_x, pos_y, area_id, num):
        self.price = price
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.area_id = area_id
        self.num = num

    def __radd__(self, other):
        return other + self.price

    def to_dict(self):
        ret = {
            u'price': self.price,
            u'pos_x': self.pos_x,
            u'pos_y': self.pos_y,
            u'area_id': self.area_id,
            u'unit': self.num,
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

    def calc(self):
        self.sale_data = sorted(self.sale_data, key=lambda u: u.price)
        min_price = self.sale_data[0].price
        max_price = self.sale_data[-1].price
        ave = sum(self.sale_data)/len(self.sale_data)
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
