from dataclasses import dataclass

@dataclass
class Word:
    word: str
    definitions: list[str]
    usage: str
