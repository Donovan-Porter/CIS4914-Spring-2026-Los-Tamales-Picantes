from minigames.matching import MemoryGame
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import uuid


# store each unique matching game
games = {}

# load the .env that has the token
load_dotenv()

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

def handle_hint_image(game_id, row, col):
    '''
    handle hint button being click and generating an image

    :param game_id: game id
    :param row: row number
    :param col: col number
    '''
    game = games.get(game_id)

    english_word = game.get_english_word_for_card(row, col)

    image_path = _image_generation(english_word)

    return image_path

def _open_file(image_path):
    '''
    see if the image file exsists and return True or False

    :param image_path: path of the image file
    '''    
    # this is ideal hahaha we don't have to wait to run the model again
    try:
        with open(image_path, "r") as file:
            return True

    # this is ideal number two we run the new word
    except FileNotFoundError:
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def _image_generation(word):
    '''
    handle getting the image from the offsite model
    save it locally

    :param word: english word 
    '''

    image_path = f"minigames\\images\\{word}.png"

    #TODO: maybe this is not needed because if the picture is bad...
    # try to see if the image has already been generated to save time
    file_created = _open_file(image_path)
    if file_created:
        return image_path
    
    # get the token
    HF_TOKEN = os.getenv("HF_TOKEN")

    # prompt doesn't want just the word printed
    neg_prompt = "text, words"

    prompt_base = f"""
    Subject Definition: {word}
    Action and Context: Depict a capybara acting {word}
    Environment and Setting: Morning time
    Visual Style and References: 2000's art style, illustrative 
    Lighting and Color: dramatic
    Camera and Composition: framing
    Quality and Realism Control: cinematic polish 
    """
    # different models that both work serverless
    # model_id = "black-forest-labs/FLUX.1-schnell" # this one is nicer quality
    model_id = "stabilityai/stable-diffusion-xl-base-1.0" # less nice but works

    
    # get the image
    client = InferenceClient(token=HF_TOKEN)
    image = client.text_to_image(
        model=model_id,
        negative_prompt=neg_prompt,
        prompt=prompt_base)

    image.save(image_path)
    return image_path
