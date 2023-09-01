import json
import os
from db_opener import read_db
from export import AnkiExport
import concurrent.futures
from dictionaries import MultiDict
dictionary = MultiDict()

print("Eyal, reminder: execute this script with python3.9 using the bin python3, if it's done already you can ignore this message")

def fetch_definitions(word, lang, dictionary):
    word.definitions = dictionary.meanings(word.word, lang)
    print(word)


def save_processed(words):
    processed_file = "processed.json"
    try:
        processed = json.load(open(processed_file))
    except FileNotFoundError:
        processed = []

    processed.extend(words)
    processed = list(set(processed))
    json.dump(processed, open(processed_file, 'w'))

def load_processed():
    processed_file = "processed.json"
    try:
        processed = json.load(open(processed_file))
    except FileNotFoundError:
        processed = []
    return processed


def main():

    dicts = read_db()
    processed = set(load_processed())

    # Enrich words
    max_threads = 100
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for lang, words in dicts.items():
            for w in words:
                if w.word in processed:
                    continue
                task = executor.submit(fetch_definitions, w, lang, dictionary)
                futures.append(task)

    concurrent.futures.wait(futures)

    if not os.path.exists('decks'):
        os.mkdir('decks')

    for lang, words in dicts.items():
        deck_name = f"Kindle-Vocabulary-{lang}"
        anki = AnkiExport(deck_name)
        c = 0
        for w in words:
            if w.word in processed:
                continue
            anki.add_word(w.word, w.definitions, w.usage)
            c += 1

        anki.write_file(outfile=f"decks/{deck_name}.apkg")
        print(f"Added {c} words to {lang}")

    processed = []
    for words_list in dicts.values():
        processed.extend([w.word for w in words_list])

    save_processed(processed)
    print("Done :)")


if __name__ == "__main__":
    main()
