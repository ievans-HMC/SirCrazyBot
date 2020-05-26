# Author: Isaiah Evans

import re

class TowerOfHanoi:
    
    def __init__(self, height: int):
        """
        Create a Tower of Hanoi game with the specified height
        """
        if height < 1:
            raise ValueError("Tower must have a positive height")
        self.max_height = height
        self.left_tower = []
        self.middle_tower = []
        self.right_tower = [i for i in range(height,0,-1)]
        self.num_moves = 0

        # print(self.right_tower)

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
        tower += "```"
        return tower

    def game_over(self):
        """
        Checks whether the game is over.
        """
        return self.middle_tower == [] and self.right_tower == []

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
                    print("That is not a valid move! Please try again")
                    return False
            else:
                dst.append(src.pop())
                return True
        else:
            print("That is not a valid move! Please try again")
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

    def play(self):
        print(self)
        print(  "Rules: L = left tower | M = middle tower | R = right "
                "tower \n"
                "Move by typing the tower you want to move from followed "
                "by the tower you want to move to \n"
                "e.g. 'LM' would move the top of the left tower onto the "
                "middle tower")

        while not self.game_over():
            move = False
            while not move:
                move_string = input("Make a move!\n")
                while not re.match(r"^[LMRlmr]{2}$",move_string):
                    move_string = input("That is not a move!\n")
                src = self.get_tower(move_string[0])
                dst = self.get_tower(move_string[1])
                move = self.move(src,dst)
            self.num_moves += 1
            print(self)
        print(f"Congratulations! You won in {self.num_moves} turns!")
        