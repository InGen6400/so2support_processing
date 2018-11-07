
class PriceData(object):
    min = -1
    max = -1
    ave = -1
    top5 = [-1, -1, -1, -1, -1]

    def __init__(self, min_in, max_in, ave, top5):
        self.min = min_in
        self.max = max_in
        self.ave = ave
        self.top5 = top5

    @staticmethod
    def from_dict(source):
        price_data = PriceData(source[u'min'], source[u'max'], source[u'ave'], source[u'top5'])
        return price_data

    def to_dict(self):
        ret = {
            u'min': self.min,
            u'max': self.max,
            u'ave': self.ave,
            u'top5': self.top5
        }
        return ret

    def __repr__(self):
        return u'PriceData(min:{} max:{} ave:{} top5:{})'.format(
            self.min, self.max, self.ave, self.top5)
