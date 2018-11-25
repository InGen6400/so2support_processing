
class ItemData(object):

    def __init__(self, id_in, name, category, scale, sort):
        self.id = id_in
        self.name = name
        self.category = category
        self.scale = scale
        self.sort = sort

    @staticmethod
    def from_dict(source):
        item_data = ItemData(source['id'], source[u'name'], source[u'category'], source[u'scale'], source[u'sort'])
        return item_data

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'name': self.name,
            u'category': self.category,
            u'scale': self.scale,
            u'sort': self.sort
        }
        return dest

    def __repr__(self):
        return u'ItemData(id:{} name:{} category:{} scale:{} sort:{})'.format(
            self.id, self.name, self.category, self.scale, self.sort)
