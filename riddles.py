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
        "logik": {
            1: [
                {"question": "Welche Aussage ist korrekt?\n  A) Wasser ist trocken\n  B) Feuer ist heiß\n  C) Schnee ist schwarz", "answer": "B"},
                {"question": "Welche Aussage ist wahr?\n  A) 2 + 2 = 5\n  B) 2 + 2 = 4\n  C) 2 + 2 = 3", "answer": "B"}
            ],
            2: [
                {"question": "Welche Aussage ist richtig?\n  A) Die Erde ist rund\n  B) Die Erde ist flach\n  C) Die Erde ist eckig", "answer": "A"},
                {"question": "Welche Aussage ist korrekt?\n  A) Feuer ist kalt\n  B) Eis ist heiß\n  C) Wasser ist flüssig", "answer": "C"}
            ],
            3: [
                {"question": "Welche Aussage ist korrekt?\n  A) Alle Vögel können fliegen\n  B) Pinguine können nicht fliegen\n  C) Fische können fliegen", "answer": "B"},
                {"question": "Welche Aussage ist wahr?\n  A) Bäume produzieren Sauerstoff\n  B) Autos produzieren Sauerstoff\n  C) Steine produzieren Sauerstoff", "answer": "A"}
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
        "rätsel": {
            1: [
                {
                    "question": "Was hat einen Kopf und einen Schwanz, aber keinen Körper?",
                    "answer": "Münze",
                    "hint": "Oft in Spielen als Einsatz verwendet."
                },
                {
                    "question": "Ich bin leicht wie eine Feder, aber niemand kann mich halten. Was bin ich?",
                    "answer": "Atem",
                    "hint": "Du brauchst mich zum Leben."
                }
            ],
            2: [
                {
                    "question": "Ich gehe, ohne zu laufen, und habe ein Bett, schlafe aber nie. Was bin ich?",
                    "answer": "Fluss",
                    "hint": "Ich fließe unaufhörlich."
                },
                {
                    "question": "Ich spreche ohne Mund und höre ohne Ohren. Was bin ich?",
                    "answer": "Echo",
                    "hint": "Höre genau hin."
                }
            ],
            3: [
                {
                    "question": "Ich kann fliegen ohne Flügel und weinen ohne Augen. Was bin ich?",
                    "answer": "Wolke",
                    "hint": "Ich schwebe am Himmel und bringe oft Regen."
                },
                {
                    "question": "Ich bin immer hungrig und muss ständig essen, doch wenn ich trinke, sterbe ich. Was bin ich?",
                    "answer": "Feuer",
                    "hint": "Ich verbrenne, aber bin kein Lebewesen."
                }
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
        if typ in ["arithmetik", "binär", "zahlenfolge", "logik", "rätsel"]:
            answer = task["answer"].upper().strip()
            lines = task["question"].split("\n")
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
