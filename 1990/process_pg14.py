import StringIO

class ListOfLines(object):
    def __init__(self, source, lo, hi):
        self._source = source
        self._lo = lo
        self._hi = hi
        self._counter = 0
        self._line = ''

    def _next_line(self):
        while self._counter < self._lo:
            self._line = self._source.readline()
            self._counter += 1
        if len(self._line) > 0 and self._counter < self._hi:
            self._line = self._source.readline()
            self._counter += 1
        else:
            self._line = ''
        return self._line

    def _get_info(self, separator, remark):
        paragraph = list()
        paragraph.append(self._line.strip())
        self._next_line()
        while len(self._line) > 0 and not self._line == '\r\n' and not self._line[0] == remark:
            paragraph.append(' ' + self._line.strip())
            self._next_line()
        source = ' '.join(paragraph)
        divisor = source.find(separator)
        if divisor < 1:
            return ['error', source]
        else:
            return [source[:divisor], source[divisor+1:]]

    def find(self, start_label, separator, remark, cube):
        self._next_line()
        while len(self._line) > 0 and not separator in self._line and not self._line[0] == remark:
            self._next_line()
        info = self._get_info(separator, remark)
        while not info[0] == start_label:
            while len(self._line) > 0 and not separator in self._line and not self._line[0] == remark:
                self._next_line()
            info = self._get_info(separator, remark)
        store = cube.put(info)
        while len(self._line) > 0:
            while len(self._line) > 0 and not separator in self._line:
                self._next_line()
            if len(self._line) > 0:
                info = self._get_info(separator, remark)
                if info[0] == start_label:
                    store = cube.put(info)
                else:
                    store.put(info)

class Store(object):

    def __init__(self):
        self._info = dict()
        self._order = list()

    def put(self, info):
        key = info[0]
        value = info[1]
        k = key.strip()
        v = value.strip()
        self._info[k] = v
        self._order.append(k)

    def show(self, margin):
        for key in self._order:
            value = self._info[key]
            print margin, key #, ': ', self._info[key]

class Cube(object):

    def __init__(self):
        self._info = dict()

    def put(self, info):
        label = info[0]
        whole_key = info[1]
        index = whole_key.find('Note:')
        key = whole_key[:index] if index > 0 else whole_key
        key = key.strip()
        try:
            x = self._info[key]
        except KeyError:
            value = Store()
            self._info[key] = value
            value.put(['whole_key', whole_key])
            return value
        else:
            raise KeyError('Cube: there is a value for this key = %s' % key)

    def get(self, key):
        return self._info[key]
    
    def show(self):
        for key, value in self._info.iteritems():
            print key
            value.show('   ')

    def generate_table(self, target_filename):
        with open(target_filename, 'w') as target:
            keys = sorted(self._info.keys())
            store = self._info[keys[0]]
            reference_cols = store._order
            row = StringIO.StringIO()
            row.write('"Country"')
            for a_col in reference_cols[1:]:
                row.write(', "%s"' % a_col)
            row.write(', "differences"\n')
            target.write(row.getvalue())
            row.close()
            for a_key in keys:
                store = self._info[a_key]
                differences = 0
                row = StringIO.StringIO()
                row.write('"%s"' % a_key)
                for a_col in reference_cols[1:]:
                    try:
                        value = store._info[a_col]
                        row.write(', "%s"' % value)
                    except KeyError:
                        differences += 1
                        row.write(', "No key"')
                value = len(reference_cols) - len(store._order)
                if value > 0:
                    differences += value
                elif value < 0:
                    differences -= value
                row.write(', "%d"\n' % differences)
                target.write(row.getvalue())
                row.close()
    
source_filename = '/home/datasets/Documents/cia/data/pg14.txt'
cube = Cube()
with open(source_filename, 'r') as source:
    lines = ListOfLines(source, 732, 52159)
    lines.find('Country', ':', '-', cube)
cube.show()
cube.generate_table('./cia_1990_pg14.csv')