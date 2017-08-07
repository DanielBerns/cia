import pdb
import StringIO

class ListOfLines(object):
    def __init__(self, source):
        self._source = source
        self._counter = 0
        self._selection = ''
        self._chunk = ''
        self._prefixes = list()

    def _select(self, source):
        self._selection = source.replace('\r', ' ').replace('\n', ' ').strip()
        return self._selection

    def get_line(self, number):
        line = ''
        while number > self._counter:
            line = self._source.readline()
            self._counter += 1
        return line

    def select_line(self, number):
        line = self.get_line(number)
        return self._select(line.strip())
    
    def get_paragraph(self, lo, hi, no_empty_lines=True):
        paragraph = list()
        for i in xrange(lo, hi+1):
            xxx = self.get_line(i)
            yyy = xxx.strip()
            if no_empty_lines and len(yyy) == 0:
                continue
            paragraph.append(yyy) 
        return paragraph

    def select_paragraph(self, lo, hi, no_empty_lines=True):
        paragraph = self.get_paragraph(lo, hi, no_empty_lines)
        return self._select(' '.join(paragraph))

    def counter(self):
        return self._counter

    def selection(self):
        return self._selection

    def item(self):
        return (self._counter, self._line)

    #def add_search_prefix(self, prefix):
        #self._prefixes.append(prefix)

    #def get_chunk_line(self):
        #line = None
        #line = self._source.readline()
        #if line == '':
            #raise ValueError()
        #else:
            #self._counter += 1
            #return line.strip()

    #def get_chunk(self):
        #last_chunk = False
        #paragraph = list()
        #line = self.get_chunk_line()
        #while line == '':
            #line = self.get_chunk_line()
        #lo = self._counter - 1
        #splits = line.split(':')
        #key = splits[0]
        #paragraph.append(splits[1])
        #try:
            #while line != '':
                #line = self.get_chunk_line()
                #paragraph.append(line)
        #except ValueError:
            #self._counter += 1
            #last_chunk = True
        #hi = self._counter - 1
        #source = ' '.join(paragraph)
        #return key, lo, hi, source, last_chunk

    #def search_prefixes(self):
        #index = 0
        #prefix = self._prefixes[index]
        #while self.get_chunk():
            #if self._chunk.startswith(prefix):
                #key = prefix
                #value = chunk[0:len(prefix)].strip()
                #yield key, value
                #index += 1
                #prefix = self._prefixes[index]


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
        for key in list_of_keys:
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

DIGITS = '1234567890'

def split_by_chars(source, chars):
    pos = 0
    for c in source:
        if c in chars:
            break
        else:
            pos += 1
    return source[:pos].strip(), source[pos:].strip()

def parse_fields(source, separator=';'):
    return source.split(separator)

def parse_splits(source, separator=':'):
    return [s.strip() for s in source.split(separator)]

def extract_fields_and_splits(store, source, _parse_fields=parse_fields, _parse_splits=parse_splits):
    fields = _parse_fields(source)
    for a_field in fields:
        splits = _parse_splits(a_field)
        store.put(splits[0], splits[1])

def extract_splits(store, source, _parse_splits=parse_splits):
    splits = _parse_splits(source)
    store.put(splits[0], splits[1])

def extract_phrases(store, source, splits_separator=':', values_separator=';'):
    splits = source.split(splits_separator)
    key = splits[0]
    values = splits[1].split(values_separator)
    for counter, phrase in enumerate(values):
        country_info.put(key + '_' + repr(counter), phrase)

class SplitsStore(object):
    def __init__(self):
        self._key = ''
        self._value = ''
    
    def put(self, key, value):
        self._key = key
        self._value = value
    
    def key(self):
        return self._key

    def value(self):
        return self._value
    

def after(prefix, source):
    target = source[len(prefix):]
    return target.strip()

def mycsv(array):
    target = StringIO.StringIO()
    target.write('"%s"' % array[0])
    for item in array[1:]:
        target.write(', "%s"' % item.strip())
    result = target.getvalue()
    target.close()
    return result

PG_TITLE = 'pg_title'
PG_AUTHOR = 'pg_author'
PG_POSTING_DATE = 'pg_posting_date'
CIA_RELEASE_DATE = 'cia_release_date'
LANGUAGE = 'language'
PRODUCED_BY = 'Produced by'
CIA_CONTACT_INFO = 'cia_contact_info'
GEO_ENTITIES = 'geo_entities'
ABBREVIATURES = 'abbreviatures'

source_filename = '../data/pg14.txt'
doc = Store()
replacements = Store()
definitions = Store()
entities = Cube()
with open(source_filename, 'r') as source:
    lines = ListOfLines(source)
    extract_splits(doc, lines.get_line(10))
    extract_splits(doc, lines.get_line(12))
    extract_splits(doc, lines.get_line(14))
    extract_splits(doc, lines.get_line(15))
    doc.put(PRODUCED_BY, after(PRODUCED_BY, lines.get_line(25)))
    
    paragraph = lines.get_paragraph(43, 46)
    doc.put(CIA_CONTACT_INFO, mycsv(paragraph))

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

    entities.create_list(paragraph)

    paragraph = lines.get_paragraph(357, 387)
    merge_entry(paragraph, "PDRY      People's Democratic Republic of Yemen {Yemen", "(Aden) or South Yemen}")

    for item in paragraph:
        point = item.find(' ')
        key = item[:point]
        value = item[point:].strip()
        replacements.put(key, value)

    extract_splits(definitions, lines.select_paragraph(389, 392))
    extract_splits(definitions, lines.select_paragraph(403, 404))
    extract_splits(definitions, lines.select_paragraph(406, 413))
    extract_splits(definitions, lines.select_paragraph(415, 420))
    extract_splits(definitions, lines.select_paragraph(422, 423))
    extract_splits(definitions, lines.select_paragraph(425, 440))
    extract_splits(definitions, lines.select_paragraph(442, 450))
    extract_splits(definitions, lines.select_paragraph(452, 463))
    extract_splits(definitions, lines.select_paragraph(522, 523))
    extract_splits(definitions, lines.select_paragraph(525, 527))
    extract_splits(definitions, lines.select_paragraph(529, 543))
    extract_splits(definitions, lines.select_paragraph(545, 548))
    extract_splits(definitions, lines.select_paragraph(550, 618))
    extract_splits(definitions, lines.select_paragraph(620, 622))
    extract_splits(definitions, lines.select_paragraph(624, 633))
    extract_splits(definitions, lines.select_paragraph(635, 641))
    extract_splits(definitions, lines.select_paragraph(643, 645))
    extract_splits(definitions, lines.select_paragraph(647, 648))
    extract_splits(definitions, lines.select_paragraph(650, 705))
    extract_splits(definitions, lines.select_paragraph(707, 708))
    extract_splits(definitions, lines.select_paragraph(710, 715))
    extract_splits(definitions, lines.select_paragraph(717, 720))
    extract_splits(definitions, lines.select_paragraph(722, 724))
    extract_splits(definitions, lines.select_paragraph(726, 727))

    country = SplitsStore()

    extract_splits(country, lines.get_line(733))
    country_info = entities.get(country.value())
    extract_fields_and_splits(country_info, lines.get_line(735))
    extract_splits(country_info, lines.get_line(737))

    fields = parse_fields(lines.select_paragraph(739, 740))
    splits = fields[0].split(':')
    country_info.put(splits[0], splits[1])
    fields = fields[1].split(', ')
    for item in fields:
        key, value = split_by_chars(item, DIGITS)
        country_info.put('LimitWith(' + country.value() + ', ' + key + ')', value) 
    
    extract_splits(country_info, lines.get_line(742))
    extract_splits(country_info, lines.get_line(744))

    extract_phrases(country_info, lines.select_paragraph(746, 749))

    extract_splits(country_info, lines.get_line(751))
    extract_splits(country_info, lines.get_line(753))
    extract_phrases(country_info, lines.select_paragraph(761, 762))

    splits = parse_splits(lines.get_line(767))
    items = splits[1].split(', ')
    country_info.put(splits[0], items[0])
    key, value = split_by_chars(items[1], DIGITS)
    country_info.put(splits[0] + ' ' + key, value)

    extract_splits(country_info, lines.get_line(769))
    extract_splits(country_info, lines.get_line(771))
    extract_splits(country_info, lines.get_line(773))
    extract_splits(country_info, lines.get_line(777))
    extract_splits(country_info, lines.get_line(779))
    extract_splits(country_info, lines.get_line(781))

    splits = parse_splits(lines.get_line(783))
    key = splits[0].strip()
    fields = splits[1].strip().split(';')
    splits = fields[0].split('--')
    country_info.put(key + ' ' + splits[0].strip(), splits[1].strip())
    splits = fields[1].split('--')
    country_info.put(key + ' ' + splits[0].strip(), splits[1].strip())

    extract_phrases(country_info, lines.select_paragraph(785, 786))

    splits = parse_splits(lines.get_line(788))
    items = splits[1].split(', ')
    for counter, value in enumerate(items):
        country_info.put(splits[0] + '_' + repr(counter), value)

    extract_phrases(country_info, lines.select_paragraph(790, 792))
    extract_splits(country_info, lines.get_line(794))
    extract_phrases(country_info, lines.select_paragraph(796, 798))
    extract_splits(country_info, lines.get_line(800))
    extract_splits(country_info, lines.get_line(803))
    extract_splits(country_info, lines.get_line(805))
    extract_splits(country_info, lines.get_line(807))
    extract_phrases(country_info, lines.select_paragraph(809, 815))
    extract_splits(country_info, lines.get_line(817))
    extract_splits(country_info, lines.get_line(819))
    extract_splits(country_info, lines.get_line(821))
    extract_splits(country_info, lines.get_line(823))
    extract_splits(country_info, lines.select_paragraph(825, 826))
    extract_splits(country_info, lines.select_paragraph(828, 830))
    extract_splits(country_info, lines.select_paragraph(832, 832))
    extract_phrases(country_info, lines.select_paragraph(834, 838))
    extract_phrases(country_info, lines.select_paragraph(840, 844))    
    extract_splits(country_info, lines.get_line(846))
    extract_phrases(country_info, lines.select_paragraph(848, 856))
    extract_phrases(country_info, lines.select_paragraph(865, 867))
    extract_splits(country_info, lines.get_line(897))
    extract_splits(country_info, lines.get_line(899))
    extract_splits(country_info, lines.get_line(901))
    extract_phrases(country_info, lines.select_paragraph(903, 904))
    extract_phrases(country_info, lines.select_paragraph(906, 909))
    extract_phrases(country_info, lines.select_paragraph(911, 913))
    extract_splits(country_info, lines.get_line(901))
doc.show()
replacements.show()
definitions.show()
country_info.show()