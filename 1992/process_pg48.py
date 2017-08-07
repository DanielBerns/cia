import pdb
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
        if len(self._line) > 0:
            if self._counter < self._hi:
                self._line = self._source.readline()
                self._counter += 1
            else:
                self._line = ''
                self._counter = self._hi
        else:
            self._line = ''
            self._counter = self._hi
        return self._line

    def _get_section(self, cube, section):
        while not self._line == '\r\n':
	    field = self._line.strip()
	    source = list()
	    self._next_line()
	    while self._line.startswith('    '):
                source.append(' ' + self._line.strip())
                self._next_line()
            value = ' '.join(source)
            cube.put(section, field, value)

    def find(self, cube):
        self._next_line()
        while len(self._line) > 0:
            while len(self._line) > 0 and not self._line.startswith(':'):
                self._next_line()
            if len(self._line) > 0:
                section = self._line.strip()
                self._next_line()
                while not self._line.endswith(':\r\n'):
                    self._next_line()
                self._get_section(cube, section)
                

class Store(object):

    def __init__(self):
        self._info = dict()
        self._order = list()

    def put(self, key, value):
        k = key.strip()
        v = value.strip()
        p = 0
        try:
            x = self._info[k]
            p = len(x)
            x.append(v)
        except KeyError:
            x = list()
            self._info[k] = x
            x.append(v)
        self._order.append((k, p))

    def show(self, margin):
        for key, position in self._order:
            value = self._info[key][position]
            print margin, key, ': ', value


import datetime

class Cube(object):

    def __init__(self):
        self._current_section = ''
        self._current_store = None
        self._info = list()

    def put(self, section, field, value):
        if len(section) > 0:
            if not self._current_section == section:
                self._current_store = Store()
                self._current_section = section
                self._info.append((self._current_section, self._current_store))
            self._current_store.put(field, value)

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



source_filename = '/home/datasets/Documents/cia/data/pg48.txt'
cube = Cube()
with open(source_filename, 'r') as source:
    lines = ListOfLines(source, 61, 59262)
    lines.find(cube)
cube.show()
pdb.set_trace()
cube.generate_table('./cia_1992_pg48.csv')