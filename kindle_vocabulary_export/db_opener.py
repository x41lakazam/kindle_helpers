from pathlib import Path
import sqlite3
from collections import defaultdict

from common import Word





def read_db(kindle_path="/media/x41/Kindle") -> dict[str, list[Word]]:
    """Return a dict where key is a language code and value is a list of tuples in format (word,
    definitions, usage)"""

    words = defaultdict(list)

    db_path = Path(kindle_path).joinpath("system/vocabulary/vocab.db")
    try:
        con = sqlite3.connect(db_path)
    except Exception as e:
            print(e)
            return {}

    cur = con.cursor()
    r = cur.execute("SELECT word_key, usage, book_key FROM lookups")

    for word_key, usage, book_key in r.fetchall():
        book_name = book_key.split(":")[0]
        lang, word = word_key.split(":")
        #usage = usage.replace(word, f"<div style='font-weight: bold>{word}</div>")
        usage = f"{usage} ({book_name})"
        words[lang].append(
            Word(word=word, definitions=[], usage=usage)
        )

    return words
