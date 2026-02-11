import random
import string
import json


class Card:
    def __init__(self, eng, spn):
        self.english = eng
        self.spanish = spn
        self._is_matched = False
        self._is_spanish = False

    def compare(self, incoming_word):
        if self.english == incoming_word or self.spanish == incoming_word:
            return True
        return False
    
    def change_matched_to_true(self):
        self._is_matched = True

    def is_matched(self):
        return self._is_matched
    
    def set_spanish_card(self):
        self._is_spanish = True

    def is_spanish_card(self):
        return self._is_spanish
    
    def get_word(self):
        if self._is_spanish:
            return self.spanish
        return self.english
    

class MemoryGame:
    def __init__(self, size=4, chapter_num=1):
        '''
        Set up for the matching game
        
        :param size: size of the board
        :param chapter_num: chapter to load 
        '''
        # width & height of board
        self.size = size

        # all the data that is loaded from the file
        self.data_pool = []

        self.total_pairs = 0
        self.game_board = []

        # running list of matched cards
        self.matched = []

        # kept track of the matches
        self.first_card = None
        self.second_pick = None

        # how many matches we found
        self.matches_found = 0

        # set up the board
        self.string_board = self._create_board(chapter_num)

    def get_string_board_from_game_board(self, game_board):
        '''
        Create a 2D list of strings from a 2D list of Card objects
        
        :param game_board: 2D list of Cards

        '''
        string_board = []
        for row in game_board:
            cur_row = []
            for cur_card in row:
                cur_row.append(cur_card.get_word())
            string_board.append(cur_row)
        return string_board

    def get_data_from_file(self, chapter_num, is_vocab):
        '''
        Parse the data from the files
        
        :param chapter_num: chapter number that was selected
        :param is_vocab: is this a vocabulary file
        '''
        # TODO: handle spanish 1 and spanish 2
        
        if is_vocab:
            self._handle_vocab_file(chapter_num)
        else:
            self._handle_grammar_file(chapter_num)

    def _handle_vocab_file(self, chapter_num):
        '''
        Parsing the data from a vocab file
        
        :param chapter_num: chapter select
        '''
        base_vocab_string = "static\\learning-resources\\spn1130-vocab\\"

        filename = base_vocab_string + f"vocab{chapter_num}.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        groups = data["groups"]
        for each_group in groups:
            # get the vocab
            vocab_list = each_group["vocabulary"]
            for each_pair in vocab_list:
                spanish = each_pair["es"]
                english = each_pair["en"]
                
                self.data_pool.append(Card(english,spanish))

        # for card in self.data_pool:
        #     print("English: " + card.english + " || Spanish: " + card.spanish)

    def _handle_grammar_file(self, chapter_num):
        '''
        Parsing the data from a grammar file
        
        :param chapter_num: chapter select
        '''
        base_grammar_string = "static\\learning-resources\\spn1130-grammar\\"

        filename = base_grammar_string + f"vocab{chapter_num}.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # TODO: update to handle grammar structure

        # groups = data["groups"]
        # for each_group in groups:
        #     # get the vocab
        #     vocab_list = each_group["vocabulary"]
        #     for each_pair in vocab_list:
        #         spanish = each_pair["es"]
        #         english = each_pair["en"]
                
        #         self.data_pool.append(Card(english,spanish))

        for card in self.data_pool:
            print("English: " + card.english + " || Spanish: " + card.spanish)


    def _create_board(self, chapter_num):
        '''
        Create a shuffled board
        
        :param chapter_num: chapter select

        '''
        # how many pairs are needed?
        self.total_pairs = (self.size * self.size) // 2

        # fill in the matching list with false
        for row_index in range(self.size):
            row = []
            for col_index in range(self.size):
                row.append(False)
            
            # Add the row to the revealed board
            self.matched.append(row)

        # load the file
        # TODO: test test test
        is_vocab = True
        self.get_data_from_file(chapter_num, is_vocab)                    

        # shuffle this stuff
        random.shuffle(self.data_pool)
        
        # pick cards
        temp_board = []
        for count in range(self.total_pairs):
            # add eng and span to game board
            current_card = (self.data_pool[count])

            spanish_card = Card(current_card.english, current_card.spanish)
            spanish_card.set_spanish_card()
            english_card = Card(current_card.english, current_card.spanish)

            temp_board.append(spanish_card)
            temp_board.append(english_card)
            
        # shuffle game board
        random.shuffle(temp_board)

        # make a 2D list of Card objects
        cur_idx = 0
        for row in range(self.size):
            current_row = []
            for col in range(self.size):
                current_row.append((temp_board[cur_idx]))
                cur_idx += 1
            self.game_board.append(current_row)

        # get the 2D string board
        string_board = self.get_string_board_from_game_board(self.game_board)

        return string_board

    def click_card(self, row, col):
        '''
        Handle a card being clicked
        Handle comparing the cards clicked
        
        :param row: row for the clicked card
        :param col: col for the clicked card
        '''
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
        if self.string_board[first_row][first_col] == self.string_board[second_row][second_col]:
            # set that they have been matched
            self.matched[first_row][first_col] = True
            self.matched[second_row][second_col] = True
            self.matches_found += 1
            game_state = "match"
        
        # they dont match
        else:
            game_state = "no_match"
        
        return {"result": game_state, "state": self.state()}

    
    def state(self):
        '''
        Get the game state for the frontend  

        '''
        game_state = {}

        # get all card values
        game_state["board"] = self.string_board

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
        