import genanki
import random

class AnkiExport:

    model = genanki.Model(
        1607399111,
        'Vocabulaire',
        fields=[
            {'name': 'Word'},
            {'name': 'Definition'},
            {'name': 'Usage'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Word}}',
                'afmt': 'Definition: {{Definition}} <br><br> Usage: {{Usage}}',
            },
        ]
    )
    def __init__(self, deck_name):
        self.model_id = random.randrange(1 << 30, 1 << 31)

        self.deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
            deck_name
        )

    def add_word(self, word, meanings, usage=''):
        usage = usage.replace(word, f'<span style="font-weight: bold;">{word}</span>')
        note = genanki.Note(
            model=self.model,
            fields=[word, '<br>'.join(meanings), usage]
        )
        self.deck.add_note(note)

    def write_file(self, outfile='output.apkg'):
        genanki.Package(self.deck).write_to_file(outfile)




