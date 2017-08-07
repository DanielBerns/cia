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

    def _get_level(self, level, tag):
        paragraph = list()
        paragraph.append(self._line.strip())
        self._next_line()
        while len(self._line) > 0 and not self._line == '\r\n' and not self._line[0] == tag:
            paragraph.append(' ' + self._line.strip())
            self._next_line()
        source = ' '.join(paragraph)
        value = source[len(level):]
        return value

    def find(self, first_level, second_level, third_level, terminator, tag, separator, cube):
        self._next_line()
        while len(self._line) > 0 and not self._line.startswith(first_level):
            self._next_line()
        value = self._get_level(first_level, tag)
        store = cube.put(['Country', value])
        while len(self._line) > 0:
            while len(self._line) > 0:
                if self._line.startswith(third_level):
                    paragraph = self._get_level(third_level, tag)
                    index = paragraph.find(separator)
                    if index == -1:
                        info = ['error', paragraph]
                    else:
                        info = [paragraph[:index], paragraph]
                    store.put(info)
                elif self._line.startswith(terminator):
                    # pdb.set_trace()
                    self._next_line()
                elif self._line.startswith(first_level):
                    # pdb.set_trace()
                    value = self._get_level(first_level, tag)
                    store = cube.put(['Country', value])
                else:
                    self._next_line()

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
        print info
        # pdb.set_trace()
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
            print 'info ', info
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



source_filename = '/home/datasets/Documents/cia/data/pg25.txt'
cube = Cube()
with open(source_filename, 'r') as source:
    lines = ListOfLines(source, 732, 52159)
    lines.find('_@_', '_*_', '_#_', '_%_', '_', ':', cube)
cube.show()
cube.generate_table('./cia_1991_pg25.csv')