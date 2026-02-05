import random
import string

class MemoryGame:
    def __init__(self, size=4):
        # width & height of board
        self.size = size

        self.cardValues = []
        self.total_pairs = 0

        # running list of matched cards
        self.matched = []

        # kept track of the matches
        self.first_card = None
        self.second_pick = None

        # how many matches we found
        self.matches_found = 0

        # set up the board
        self.board = self._create_board()


    # create a shuffled board
    def _create_board(self):
        
        # how many pairs are needed?
        self.total_pairs = (self.size * self.size) // 2

        # fill in the matching list with false
        for row_index in range(self.size):
            row = []
            for col_index in range(self.size):
                row.append(False)
            
            # Add the row to the revealed board
            self.matched.append(row)
        

        # test to handle hard size board
        test = string.ascii_uppercase + string.ascii_lowercase

        # only add the amount of letters we need
        for count in range(self.total_pairs):
            self.cardValues.append(test[count])

        # we need pairs
        cards = self.cardValues * 2

        # shuffle this stuff
        random.shuffle(cards)

        # return the shuffled list as a 2D array
        shuffled_board = []
        for row_index in range(self.size):
            start = row_index * self.size
            end = start + self.size

            row = cards[start:end]
            shuffled_board.append(row)
        
        return shuffled_board

    def click_card(self, row, col):
        game_state = None

        # ignore clicks on already matched cards
        if self.matched[row][col]:
            return

        # first card
        if self.first_card is None:
            self.first_card = (row, col)
            return {"result": game_state, "state": self.state()}

        # second card has been selected
        second_row = row
        second_col = col

        # get first card info        
        first_row, first_col = self.first_card
        self.first_card = None


        # do they match
        if self.board[first_row][first_col] == self.board[second_row][second_col]:
            # set that they have been matched
            self.matched[first_row][first_col] = True
            self.matched[second_row][second_col] = True
            self.matches_found += 1
            game_state = "match"
        
        # they dont match
        else:
            game_state = "no_match"
        
        return {"result": game_state, "state": self.state()}

    # get the game state for the frontend
    def state(self):
        game_state = {}

        # get all card values
        game_state["board"] = self.board

        # which cards are matched
        game_state["matched"] = self.matched

        # size of the board
        game_state["size"] = self.size

        # did we match it all???
        if self.matches_found == self.total_pairs:
            game_state["finished"] = True
        else:
            game_state["finished"] = False
        

        return game_state