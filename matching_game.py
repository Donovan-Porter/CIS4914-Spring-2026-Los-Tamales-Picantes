from minigames.matching import MemoryGame
import uuid

# store each unique matching game
games = {}


def create_game(board_size, spn_lvl, chp_num, file_type):
    '''
    create a matching game

    :param board_size: size of the board that will be spawned
    :param spn_lvl: spanish course number
    :param chp_num: chapter number
    :param file_type: vocab or grammar file

    '''
    # create a memory game with the size we are looking for
    game = MemoryGame(size=board_size, spanish_level=spn_lvl, chapter_num=chp_num, file_type=file_type)

    # get the game id
    game_id = str(uuid.uuid4())
    games[game_id] = game
    return {"game_id": game_id, "state": game.state()}

def handle_click_card(game_id, row, col):
    '''
    handle a card click

    :param game_id: game id
    :param row: row number
    :param col: col number
    '''
    # get the game
    game = games.get(game_id)

    result = game.click_card(row, col)
    return result
