import traceback
import json
from collections import defaultdict

from PyDictionary import PyDictionary
from larousse_api import larousse

en_dictionary=PyDictionary()

class MultiDict():
    def __init__(self):
        self.dicts = {
            'en': EnglishDictionary(),
            #'fr': DEMDictionary("DEM-1_1.json"),
            'fr': LarousseDictionary(),
        }

    def meanings(self, word, lang):
        try:
            return self.dicts[lang].meanings(word)
        except Exception as exc:
            traceback.print_exc()
            return []


class EnglishDictionary():
    def meanings(self, word):
        r = en_dictionary.meaning(word)
        meanings = []
        for v in r.values():
            meanings.extend(v)

        return meanings


class DEMDictionary():

    def __init__(self, path, auto_load=True):
        self.path = path
        self.data: dict[str, list[dict]] = {}
        if auto_load:
            self.load()

    def unload(self):
        self.data = None

    def load(self, force_reload=True):
        if self.data and not force_reload:
            return

        self.data = self._read()

    def meanings(self, word) -> list[str]:
        return self.data[word]


    def _read(self):
        self.data = defaultdict(list)

        words_dat = json.load(open(self.path, 'r'))
        for dat in words_dat:
            w = dat["M"]["mot"]
            self.data[w].append(dat)


class LarousseDictionary():
    def meanings(self, word):
        dat = larousse.get_definitions(word)

        return dat


