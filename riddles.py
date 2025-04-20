import random
from typing import List, Tuple, Dict

class Riddle:
    # Alle Aufgaben, gruppiert nach Typ und Level
    all_tasks: Dict[str, Dict[int, List[Dict[str, str]]]] = {
        "arithmetik": {
            1: [
                {"question": "Berechne: 3 + 4 = ?", "answer": "7"},
                {"question": "Berechne: 8 - 5 = ?", "answer": "3"},
                {"question": "Berechne: 6 + 2 = ?", "answer": "8"},
                {"question": "Berechne: 9 - 3 = ?", "answer": "6"},
                {"question": "Berechne: 4 + 3 = ?", "answer": "7"}
            ],
            2: [
                {"question": "Berechne: 12 + 15 = ?", "answer": "27"},
                {"question": "Berechne: 20 - 8 = ?", "answer": "12"},
                {"question": "Berechne: 7 * 3 = ?", "answer": "21"},
                {"question": "Berechne: 18 / 2 = ?", "answer": "9"},
                {"question": "Berechne: 14 + 6 = ?", "answer": "20"}
            ],
            3: [
                {"question": "Berechne: 15 * 4 = ?", "answer": "60"},
                {"question": "Berechne: 45 / 5 = ?", "answer": "9"},
                {"question": "Berechne: 23 + 37 = ?", "answer": "60"},
                {"question": "Berechne: 50 - 17 = ?", "answer": "33"}
            ]
        },
        "binär": {
            1: [
                {"question": "Was ist die Binärdarstellung von 1?", "answer": "1"},
                {"question": "Was ist die Binärdarstellung von 2?", "answer": "10"}
            ],
            2: [
                {"question": "Was ist die Binärdarstellung von 3?", "answer": "11"},
                {"question": "Was ist die Binärdarstellung von 4?", "answer": "100"},
                {"question": "Was ist die Binärdarstellung von 5?", "answer": "101"}
            ],
            3: [
                {"question": "Was ist die Binärdarstellung von 6?", "answer": "110"},
                {"question": "Was ist die Binärdarstellung von 7?", "answer": "111"},
                {"question": "Was ist die Binärdarstellung von 8?", "answer": "1000"}
            ]
        },
        "wortspiel": {
            1: [
                {"word": "CODE"},
                {"word": "HACK"},
                {"word": "NETZ"},
                {"word": "LOGIK"},
                {"word": "SPIEL"}
            ],
            2: [
                {"word": "PROGRAMM"},
                {"word": "TECHNIK"},
                {"word": "ALGORITHMUS"},
                {"word": "VIRUS"},
                {"word": "SYSTEM"}
            ],
            3: [
                {"word": "INNOVATION"},
                {"word": "DIGITALISIERUNG"},
                {"word": "CYBERSECURITY"}
            ]
        },
        "zahlenfolge": {
            1: [
                {"question": "Welche Zahl folgt in der Reihe: 1, 2, 3, 4, ?", "answer": "5"},
                {"question": "Welche Zahl folgt in der Reihe: 2, 4, 6, 8, ?", "answer": "10"}
            ],
            2: [
                {"question": "Welche Zahl folgt in der Reihe: 3, 6, 9, 12, ?", "answer": "15"},
                {"question": "Welche Zahl folgt in der Reihe: 5, 10, 15, 20, ?", "answer": "25"}
            ],
            3: [
                {"question": "Welche Zahl folgt in der Reihe: 8, 13, 18, 23, ?", "answer": "28"},
                {"question": "Welche Zahl folgt in der Reihe: 2, 3, 5, 8, ?", "answer": "13"}
            ]
        },
        "geografie": {
            1: [
                {"question": "Was ist die Hauptstadt von Frankreich?", "answer": "PARIS", "hint": "Eiffelturm und Croissants."},
                {"question": "Welche Hauptstadt hat Deutschland?", "answer": "BERLIN", "hint": "Brandenburger Tor."}
            ],
            2: [
                {"question": "Was ist die Hauptstadt von Australien?", "answer": "CANBERRA", "hint": "Nicht Sydney."},
                {"question": "Welche Stadt ist Hauptstadt von Japan?", "answer": "TOKYO", "hint": "Metropole mit Shibuya-Kreuzung."}
            ],
            3: [
                {"question": "Wie heisst die Hauptstadt von Kasachstan seit 1997?", "answer": "ASTANA", "hint": "Ehemals Nursultan."},
                {"question": "Welche Stadt liegt bei 51° N, 0° E?", "answer": "LONDON", "hint": "Big Ben."}
            ]
        },
        "allgemeinwissen": {
            1: [
                {"question": "Was ist die chemische Formel von Wasser?\n  A) H₂O   B) CO₂   C) O₂", "answer": "A", "hint": "Man kennt es als Lebenselixier."},
                {"question": "Wie viele Kontinente gibt es?", "answer": "7", "hint": "Afrika, Europa, Asien…"}
            ],
            2: [
                {"question": "Wer malte die Mona Lisa?\n  A) Van Gogh   B) Da Vinci   C) Picasso", "answer": "B", "hint": "Leonardo…"},
                {"question": "In welchem Jahr begann der Zweite Weltkrieg?\n  A) 1935   B) 1939   C) 1941", "answer": "B", "hint": "1. September 1939."}
            ],
            3: [
                {"question": "Wer war die erste Bundesrätin der Schweiz?", "answer": "ELISABETH KOPP", "hint": "Name beginnt mit E."},
                {"question": "Was misst der pH‑Wert?", "answer": "SÄURE-BASE-VERHÄLTNIS", "hint": "Skala von 0 bis 14."}
            ]
        }
    }

    # Wird beim Start eines Levels mit init_tasks_for_level befüllt
    available_tasks: Dict[str, List[Dict[str, str]]] = {}

    @staticmethod
    def init_tasks_for_level(level: int) -> None:
        """
        Initialisiert die verfügbaren Aufgaben für ein gegebenes Level.
        Wenn das Level nicht 1, 2 oder 3 ist, wird Level 3 verwendet.
        """
        level_key = level if level in [1, 2, 3] else 3
        Riddle.available_tasks = {typ: list(tasks[level_key])
                                  for typ, tasks in Riddle.all_tasks.items()}

    @staticmethod
    def generate_riddle(level: int) -> Tuple[List[str], str, str]:
        """
        Generiert ein zufälliges Rätsel für das angegebene Level.
        Gibt eine Liste von Zeilen der Frage, die korrekte Antwort und einen Hinweis zurück.
        """
        if not Riddle.available_tasks:
            Riddle.init_tasks_for_level(level)
        available_types = [typ for typ, tasks in Riddle.available_tasks.items() if tasks]
        if not available_types:
            Riddle.init_tasks_for_level(level)
            available_types = list(Riddle.available_tasks.keys())
        typ = random.choice(available_types)
        task = random.choice(Riddle.available_tasks[typ])
        Riddle.available_tasks[typ].remove(task)
        # Für einfache Frage-Antwort-Typen inklusive neu hinzugefügter Kategorien
        if typ in ["arithmetik", "binär", "zahlenfolge", "geografie", "allgemeinwissen"]:
            answer = task.get("answer", "").upper().strip()
            lines = task.get("question", "").split("\n")
            hint = task.get("hint", "")
            return lines, answer, hint
        elif typ == "wortspiel":
            word = task["word"]
            scrambled = "".join(random.sample(word, len(word)))
            answer = word.upper().strip()
            lines = ["Entschlüssele das Wort:", "", "  " + scrambled]
            hint = task.get("hint", "")
            return lines, answer, hint
        else:
            return ["Kein Rätsel verfügbar."], "", ""