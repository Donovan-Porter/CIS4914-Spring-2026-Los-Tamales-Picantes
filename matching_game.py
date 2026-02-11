from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, jsonify
from flaskwebgui import FlaskUI
from minigames.matching import MemoryGame
import uuid

# store each unique matching game
games = {}

# create a matching game
def create_game(returned_size):

    # create a memory game with the size we are looking for
    game = MemoryGame(size=returned_size)

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
