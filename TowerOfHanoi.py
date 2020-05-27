# Author: Isaiah Evans

import re

class TowerOfHanoi:
    
    def __init__(self, height: int):
        """
        Create a Tower of Hanoi game with the specified height
        """
        self.max_height = height
        self.left_tower = []
        self.middle_tower = []
        self.right_tower = [i for i in range(height,0,-1)]
        self.num_moves = 0
        self.response = ""

    def __str__(self):
        """
        Represent a Tower of Hanoi as a String
        """
        tower = "```\n"
        tower += "=" * (3 * (2 * self.max_height) + 1) + "\n"
        tower += " " *  self.max_height      + "L" + " " * self.max_height
        tower += " " * (self.max_height - 1) + "M" + " " * self.max_height
        tower += " " * (self.max_height - 1) + "R" + " " * self.max_height + "\n"
        tower += "=" * (3 * (2 * self.max_height) + 1) + "\n"
        
        for i in range(1,self.max_height+1):
            tower += " "
            # Left Tower
            try:
                size = self.left_tower[self.max_height - i]
                tower += " " * (self.max_height - size)
                tower += "-" * (size - 1)
                tower += "+"
                tower += "-" * (size - 1)
                tower += " " * (self.max_height - size)
            except:
                tower += " " * (self.max_height - 1)
                tower += "|"
                tower += " " * (self.max_height - 1)
            tower += " "

            # Middle Tower
            try:
                size = self.middle_tower[self.max_height - i]
                tower += " " * (self.max_height - size)
                tower += "-" * (size - 1)
                tower += "+"
                tower += "-" * (size - 1)
                tower += " " * (self.max_height - size)
            except:
                tower += " " * (self.max_height - 1)
                tower += "|"
                tower += " " * (self.max_height - 1)
            tower += " "

            # Right Tower
            try:
                size = self.right_tower[self.max_height - i]
                tower += " " * (self.max_height - size)
                tower += "-" * (size - 1)
                tower += "+"
                tower += "-" * (size - 1)
                tower += " " * (self.max_height - size)
            except:
                tower += " " * (self.max_height - 1)
                tower += "|"
                tower += " " * (self.max_height - 1)
            tower += "\n"
        tower += "=" * (3 * (2 * self.max_height) + 1) + "\n"
        tower += "```\n"
        return tower

    def start_game(self):
        self.response = (
                "__**Rules:**__ Your goal is to move all the layers of the "
                "tower on the right to the tower on the left in as few moves "
                "as possible. You are not allowed to stack a larger layer onto "
                "a smaller one.\n"
                "__**Controls:**__ L = left tower | M = middle ""tower | R = "
                "right tower \n"
                "Move a layer by typing `hanoi` along with the tower you want "
                "to move from followed by the tower you want to move to \n"
                "e.g. `hanoi RM` would move the top of the right tower onto "
                "the middle tower.\n"
                f"**Starting game with a {self.max_height} layer tower...** "
                "The optimal solution for a tower of this height uses "
                f"{2**self.max_height - 1} moves\n"
                f"{str(self)}"
                "make a move with `hanoi LMR`"
            )
            
    def game_over(self):
        """
        Checks whether the game is over.
        """
        return (self.middle_tower == [] and self.right_tower == []) or \
            self.max_height < 1

    def move(self, src: list, dst: list):
        """
        Checks if a move is valid and makes it.

        Parameters:
            src and dst are source and destination towers.
        Returns:
            False if move is invalid, 
            otherwise, it makes the move and returns True
        """
        if src != [] and src != dst:
            if dst != []:
                if dst[-1] > src[-1]:
                    dst.append(src.pop())
                    return True
            else:
                dst.append(src.pop())
                return True
        return False
        
    def get_tower(self, tower: str):
        """
        Input:
            A string that is one of [LlMmRr]
        Returns:
            A reference to the tower corresponding to the input string
        """
        if re.match(r"^[Ll]$",tower):
            return self.left_tower
        elif re.match(r"^[Mm]$",tower):
            return self.middle_tower
        elif re.match(r"^[Rr]$",tower):
            return self.right_tower

    def take_turn(self, move_string: str):
        src = self.get_tower(move_string[0])
        dst = self.get_tower(move_string[1])
        move = self.move(src,dst)
        if not move:
            self.response = "That is not a valid move. Please try again"
            return
        self.num_moves += 1
        self.response = str(self)
        if self.game_over():
            self.response += ("Congratulations! You won in "
                             f"{self.num_moves} turns!")
        else:
            self.response += "Make a your next move!"
        