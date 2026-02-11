from minigames.matching import MemoryGame
import uuid

# store each unique matching game
games = {}

# create a matching game
def create_game(returned_size):
    # spanish levels
    # spanish_1 = "spn1130"
    # spanish_2 = "spn1131"
    # spanish_3 = "spn2200"
    # spanish_4 = "spn2201"

    # create a memory game with the size we are looking for
    game = MemoryGame(size=returned_size, spanish_level="spn1130", chapter_num=1, is_vocab=True )

    # get the game id
    game_id = str(uuid.uuid4())
    games[game_id] = game
    return {"game_id": game_id, "state": game.state()}

# handle a card click
def handle_click_card(game_id, row, col):

    # get the game
    game = games.get(game_id)

    result = game.click_card(row, col)
    return result
