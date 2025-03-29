import random

class Riddle:
    all_tasks = {
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
                {"question": "Was ist die Binärdarstellung von 2?", "answer": "10"},
                {"question": "Was ist die Binärdarstellung von 3?", "answer": "11"},
                {"question": "Was ist die Binärdarstellung von 4?", "answer": "100"},
                {"question": "Was ist die Binärdarstellung von 5?", "answer": "101"},
                {"question": "Was ist die Binärdarstellung von 6?", "answer": "110"}
            ],
            2: [
                {"question": "Was ist die Binärdarstellung von 10?", "answer": "1010"},
                {"question": "Was ist die Binärdarstellung von 12?", "answer": "1100"},
                {"question": "Was ist die Binärdarstellung von 14?", "answer": "1110"},
                {"question": "Was ist die Binärdarstellung von 15?", "answer": "1111"},
                {"question": "Was ist die Binärdarstellung von 9?", "answer": "1001"}
            ],
            3: [
                {"question": "Was ist die Binärdarstellung von 23?", "answer": "10111"},
                {"question": "Was ist die Binärdarstellung von 27?", "answer": "11011"},
                {"question": "Was ist die Binärdarstellung von 31?", "answer": "11111"}
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
                {"question": "Was hat einen Kopf, aber keinen Körper?", "answer": "Münze"},
                {"question": "Was wird nass, je mehr es trocknet?", "answer": "Handtuch"}
            ],
            2: [
                {"question": "Ich bin immer hungrig, muss ständig essen, doch wenn ich trinke, sterbe ich. Was bin ich?", "answer": "Feuer"},
                {"question": "Ich spreche ohne Mund und höre ohne Ohren. Was bin ich?", "answer": "Echo"}
            ],
            3: [
                {"question": "Ich kann fliegen ohne Flügel und weinen ohne Augen. Was bin ich?", "answer": "Wolke"}
            ]
        }
    }
    available_tasks = {}

    @staticmethod
    def init_tasks_for_level(level):
        Riddle.available_tasks = {}
        level_key = level if level in [1, 2, 3] else 3
        for typ in Riddle.all_tasks:
            Riddle.available_tasks[typ] = list(Riddle.all_tasks[typ][level_key])

    @staticmethod
    def generate_riddle(level):
        if not Riddle.available_tasks:
            Riddle.init_tasks_for_level(level)
        available_types = [typ for typ in Riddle.available_tasks if Riddle.available_tasks[typ]]
        if not available_types:
            Riddle.init_tasks_for_level(level)
            available_types = list(Riddle.available_tasks.keys())
        typ = random.choice(available_types)
        task = random.choice(Riddle.available_tasks[typ])
        Riddle.available_tasks[typ].remove(task)
        if typ in ["arithmetik", "binär", "zahlenfolge", "logik", "rätsel"]:
            answer = task["answer"].upper().strip()
            lines = task["question"].split("\n")
            return lines, answer
        elif typ == "wortspiel":
            word = task["word"]
            scrambled = "".join(random.sample(word, len(word)))
            answer = word.upper().strip()
            lines = ["Entschlüssele das Wort:", "", "  " + scrambled]
            return lines, answer
        else:
            return ["Kein Rätsel verfügbar."], ""
