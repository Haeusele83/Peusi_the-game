class Player:
    def __init__(self):
        self.level = 1
        self.solved_riddles = 0  
        self.points = 0

    def level_up(self):
        self.level += 1
        self.solved_riddles = 0  

