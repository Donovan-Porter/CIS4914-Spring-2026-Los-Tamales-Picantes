import os
import uuid
import requests
import random

from minigames.matching import MemoryGame
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

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

def _get_keyword(word):
    '''
    clean up the word and get the main idea

    :param word: english word 
    '''
    # check if it has special charater
    has_special_char = False
    special_char = ["/", "\\", ",", "("]
    for each_char in special_char:
        if word.find(each_char) != -1:
            has_special_char = True
        
    # the word is short enough
    if len(word) <= 100:
        # no special char
        if has_special_char == False:
            return word
    
    # working with a word with a special char or too long
    key_word = None

    # remove everything after comma
    clean_word = word.split(",")[0]

    # remove everything after parenthesis
    clean_word = clean_word.split("(")[0]

    clean_word = clean_word.replace("/", " ").strip()
    clean_word = clean_word.replace("\\", " ").strip()
    noneed_words = ["to", "a", "the", "of", "in", "on", "at", "for", "with", "by", "from"]
    words = clean_word.split()

    for each_word in words:
        if each_word.lower() not in noneed_words:
            key_word = each_word
            break

    # if every word was filler then just take the first one
    if key_word is None:
        key_word = words[0]

    return key_word

def _image_generation(word):
    '''
    handle getting the image from the offsite model
    handle if both models are rate limited
    save it locally

    :param word: english word 
    '''
    key_word = _get_keyword(word)
    image_path = f"minigames\\images\\{key_word}.png"


    #TODO: maybe this is not needed because if the picture is bad...
    # try to see if the image has already been generated to save time
    # file_created = _open_file(image_path)
    # if file_created:
    #     return image_path
    

    # hugging face stuff
    HF_TOKEN = os.getenv("HF_TOKEN")
    neg_prompt = "text, words"
    prompt_base = f"""
    Subject Definition: {key_word}
    Action and Context: Depict a capybara acting {key_word}
    Environment and Setting: Morning time
    Visual Style and References: 2000's art style, illustrative 
    Lighting and Color: dramatic
    Camera and Composition: framing
    Quality and Realism Control: cinematic polish"""
    models = ["black-forest-labs/FLUX.1-schnell",
              "stabilityai/stable-diffusion-xl-base-1.0"]

    client = InferenceClient(token=HF_TOKEN)

    for each_model in models:
        try:
            image = client.text_to_image(
                        model=each_model,
                        negative_prompt=neg_prompt,
                        prompt=prompt_base)
            image.save(image_path)
            return image_path
        except Exception as e:
            print(f"Model {each_model} failed: {e}")


    # both models failed so just search for the word
    try:
        PIXABAY_KEY = os.getenv("PIXABAY_KEY")
        params = {
            "key" : PIXABAY_KEY,
            "q": key_word
        }

        response = requests.get("https://pixabay.com/api/", params=params).json()
        hits = response["hits"]
        # pick a random image from the results
        img_url = random.choice(hits)["webformatURL"]

        image = Image.open(BytesIO(requests.get(img_url).content))
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Cannot find an image for {word}: {e}")
        return None