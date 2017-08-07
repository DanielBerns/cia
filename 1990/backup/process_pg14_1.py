class ListOfLines(object):
    def __init__(self, source):
        self._source = source
        self._counter = 0
        self._line = ''

    def goto(self, number):
        line = ''
        while number > self._counter:
            line = self._source.readline()
            self._counter += 1
        self._line = line
        return line
        
    def get_paragraph(self, lo, hi, no_empty_lines=True):
        paragraph = list()
        for i in xrange(lo, hi+1):
            xxx = self.goto(i)
            yyy = xxx.strip()
            if no_empty_lines and len(yyy) == 0:
                continue
            paragraph.append(yyy)
        return paragraph
    
    def get_split_n(self, i, n, sep=':'):
        xxx = self.goto(i)
        yyy = xxx.split(sep)
        zzz = yyy[n]
        return zzz.strip()

    def line(self):
        return self._line
    
    def counter(self):
        return self._counter
    
    def item(self):
        return (self._counter, self._line)

def after(line, n):
    return line[n:]

def before(line, n):
    return line[:n]

PG_TITLE = 'pg_title'
PG_AUTHOR = 'pg_author'
PG_POSTING_DATE = 'pg_posting_date'
CIA_RELEASE_DATE = 'cia_release_date'
LANGUAGE = 'language'
PRODUCTOR = 'productor'
CIA_CONTACT_INFO = 'cia_contact_info'
GEO_ENTITIES = 'geo_entities'
ABBREVIATURES = 'abbreviatures'

class Store(object):
    
    def __init__(self):
        self._info = dict()
        self._order = list()

    def put(self, key, value):
        k = key.strip()
        v = value.strip()
        self._info[k] = v
        self._order.append(k)

    def show(self):
        for key in self._order:
            value = self._info[key]
            print key, ': ', self._info[key]
        
class Cube(object):

    def __init__(self):
        self._info = dict()

    def create(self, key):
        try:
            value = self._info[key]
        except KeyError:
            value = Store()
            self._info[key] = value
            return value
        else:
            raise KeyError('Cube: there is a value for this key = %s' % key)

    def create_list(self, list_of_keys):
        for key in list_of_items:
            self.create(key)

    def get(self, key):
        return self._info[key]
    
    def update(self, key, value):
        pass
    
    def delete(self, key):
        pass


def replace_entry(paragraph, replacements, old_entry, new_entry):
    cursor = paragraph.index(old_entry)
    paragraph[cursor] = new_entry
    replacements.put(old_entry, new_entry)


def merge_entry(paragraph, old_entry_1, old_entry_2):
    cursor_1 = paragraph.index(old_entry_1)
    cursor_2 = paragraph.index(old_entry_2)
    assert(cursor_1 == cursor_2 - 1)
    new_entry = paragraph[cursor_1] + ' ' + paragraph[cursor_2]
    paragraph.remove(paragraph[cursor_1])
    paragraph.remove(paragraph[cursor_1]) # Ehhh!!! ;-)
    paragraph.insert(cursor_1, new_entry)

def extract_definition(lines, lo, hi, definitions, sep=':'):
    paragraph = lines.get_paragraph(lo, hi)
    item = paragraph[0]
    splits = item.split(sep)
    key = splits[0]
    paragraph[0] = splits[1]
    value = ' '.join(paragraph).replace('\r', ' ').replace('\n', ' ')
    definitions.put(key, value)

DIGITS = '1234567890'

def split_by_chars(source, chars):
    pos = 0
    for c in source:
        if c in chars:
            break
        else:
            pos += 1
    return source[:pos].strip(), source[pos:].strip()

def mycsv(array):
    pass

source_filename = './data/pg14.txt'
doc = Store()
replacements = Store()
definitions = Store()
entities = Cube()
with open(source_filename, 'r') as source:
    lines = ListOfLines(source)
    doc.put(PG_TITLE, lines.get_split_n(10, 1))
    doc.put(PG_AUTHOR, lines.get_split_n(12, 1))
    doc.put(PG_POSTING_DATE, before(lines.get_split_n(14, 1), -12))
    doc.put(CIA_RELEASE_DATE, lines.get_split_n(15, 1))
    doc.put(PRODUCTOR, after(lines.goto(25), 12))
    
    paragraph = lines.get_paragraph(43, 46)
    CIA_CONTACT_INFO = '"%s", "%s", "%s", "%s"' % (paragraph[0], paragraph[1], paragraph[2], paragraph[3])
    doc.put(CIA_CONTACT_INFO, CIA_CONTACT_INFO)

    paragraph = lines.get_paragraph(52, 331)

    paragraph.remove('Taiwan entry follows Zimbabwe')
    replace_entry(paragraph, replacements, 'China (also see separate Taiwan entry)', 'China')
    merge_entry(paragraph, 'German Democratic Republic', '(East Germany)')
    merge_entry(paragraph, 'Germany, Federal Republic of', '(West Germany)')
    replace_entry(paragraph, replacements, 'Israel (also see separate Gaza Strip and West Bank entries)', 'Israel')
    replace_entry(paragraph, replacements, 'Jordan (also see separate West Bank entry)', 'Jordan')
    merge_entry(paragraph, 'Pacific Islands, Trust Territory of the', '(Palau)')
    replace_entry(paragraph, replacements, 'St. Helena', 'Saint Helena')
    replace_entry(paragraph, replacements, 'St. Kitts and Nevis', 'Saint Kitts and Nevis')
    replace_entry(paragraph, replacements, 'St. Lucia', 'Saint Lucia')
    replace_entry(paragraph, replacements, 'St. Pierre and Miquelon', 'Saint Pierre and Miquelon')
    replace_entry(paragraph, replacements, 'St. Vincent and the Grenadines', 'Saint Vincent and the Grenadines')
    merge_entry(paragraph, 'Yemen Arab Republic', '{Yemen (Sanaa) or North Yemen}')
    merge_entry(paragraph, "Yemen, People's Democratic Republic of", "{Yemen (Aden) or South Yemen}")
    entities.create_list
    paragraph = lines.get_paragraph(357, 387)
    merge_entry(paragraph, "PDRY      People's Democratic Republic of Yemen {Yemen", "(Aden) or South Yemen}")
    for item in paragraph:
        point = item.find(' ')
        key = item[:point]
        value = item[point:].strip()
        replacements.put(key, value)

    extract_definition(lines, 389, 392, definitions)
    extract_definition(lines, 403, 404, definitions)
    extract_definition(lines, 406, 413, definitions)
    extract_definition(lines, 415, 420, definitions)
    extract_definition(lines, 422, 423, definitions)
    extract_definition(lines, 425, 440, definitions)
    extract_definition(lines, 442, 450, definitions)
    extract_definition(lines, 452, 463, definitions)
    extract_definition(lines, 522, 523, definitions)
    extract_definition(lines, 525, 527, definitions)
    extract_definition(lines, 529, 543, definitions)
    extract_definition(lines, 545, 548, definitions)
    extract_definition(lines, 550, 618, definitions)
    extract_definition(lines, 620, 622, definitions)
    extract_definition(lines, 624, 633, definitions)
    extract_definition(lines, 635, 641, definitions)
    extract_definition(lines, 643, 645, definitions)
    extract_definition(lines, 647, 648, definitions)
    extract_definition(lines, 650, 705, definitions)
    extract_definition(lines, 707, 708, definitions)
    extract_definition(lines, 710, 715, definitions)
    extract_definition(lines, 717, 720, definitions)
    extract_definition(lines, 722, 724, definitions)
    extract_definition(lines, 726, 727, definitions)

    country = lines.get_split_n(733, 1)
    country_info = entities.create(country)
    fields = lines.goto(735).split(';')
    splits = fields[0].split(':')
    country_info.put(splits[0], splits[1])
    splits = fields[1].split(':')
    country_info.put(splits[0], splits[1])
    splits = lines.goto(737).split(':')
    country_info.put(splits[0], splits[1])
    paragraph = lines.get_paragraph(739, 740)
    fields = (' '.join(paragraph)).split(';')
    splits = fields[0].split(':')
    country_info.put(splits[0], splits[1])
    fields = fields[1].split(', ')
    for item in fields:
        key, value = split_by_chars(item, DIGITS)
        country_info.put('LimitWith(' + country + ', ' + key + ')', value) 
    splits = lines.goto(742).split(':')
    country_info.put(splits[0], splits[1])
    splits = lines.goto(744).split(':')
    country_info.put(splits[0], splits[1])
    paragraph = lines.get_paragraph(746, 749)
    fields = (' '.join(paragraph)).split(':')
    key = fields[0]
    fields = fields[1].split(';')
    for counter, item in enumerate(fields):
        country_info.put(key + '_' + repr(counter), item) 
    splits = lines.goto(751).split(':')
    country_info.put(splits[0], splits[1])
    splits = lines.goto(753).split(':')
    country_info.put(splits[0], splits[1])
    paragraph = lines.get_paragraph(761, 762)
    splits = (' '.join(paragraph)).split(':')
    country_info.put(splits[0], splits[1])
    fields = lines.goto(767).split(', ')
    splits = fields[0].split(':')
    country_info.put(splits[0], splits[1])
    key, value = split_by_chars(fields[1], DIGITS)
    country_info.put(key, value) 
    splits = lines.goto(769).split(':')
    country_info.put(splits[0], splits[1])
    splits = lines.goto(771).split(':')
    country_info.put(splits[0], splits[1])
    splits = lines.goto(773).split(':')
    key = splits[0].strip()
    value = splits[1].strip()
    country_info.put(key, value)
    splits = lines.goto(777).split(':')
    key = splits[0].strip()
    value = splits[1].strip()
    country_info.put(key, value)
    splits = lines.goto(779).split(':')
    key = splits[0].strip()
    value = splits[1].strip()
    country_info.put(key, value)
    splits = lines.goto(781).split(':')
    key = splits[0].strip()
    value = splits[1].strip()
    country_info.put(key, value)
    splits = lines.goto(783).split(':')
    key = splits[0].strip()
    fields = splits[1].strip().split(';')
    splits = fields[0].split('--')
    country_info.put(key + ' ' + splits[0].strip(), splits[1].strip())
    splits = fields[1].split('--')
    country_info.put(key + ' ' + splits[0].strip(), splits[1].strip())
    
    
    
doc.show()
replacements.show()
definitions.show()
country_info.show()