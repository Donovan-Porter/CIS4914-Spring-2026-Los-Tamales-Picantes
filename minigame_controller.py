import os, sys
import uuid
import requests
import random
import glob
import mimetypes
import re


from minigames.matching import MemoryGame
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# store each unique game
games = {}

# load the .env that has the token
load_dotenv()

# matching game stuff
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


# flashcard stuff
def create_flashcard_game(spn_lvl, chp_num, file_type, game_mode="word_to_picture"):
    '''
    create a flashcard picture-matching game session
    reuses MemoryGame's file loading CAW CAW

    :param spn_lvl: spanish course number
    :param chp_num: chapter number
    :param file_type: vocab or grammar file
    :param game_mode: "word_to_picture" or "picture_to_word"
    '''
    # reuse MemoryGame
    loader = MemoryGame(size=4, spanish_level=spn_lvl, chapter_num=chp_num, file_type=file_type)
    all_cards = loader.data_pool

    if len(all_cards) < 4:
        return {"error": "Not enough vocabulary in this chapter."}

    random.shuffle(all_cards)

    # 5 cards for lower level
    card_count = 5
    if spn_lvl in ("spn2200", "spn2201"):
        # 10 cards for higher level
        card_count = 10
    selected_cards = all_cards[:card_count]

    # build a clean list of word pairs from the selected Card objects
    pairs = []
    for card in selected_cards:
        pair = {"english": card.english, "spanish": card.spanish}
        pairs.append(pair)
 
    # keep all the vocab available
    # this is so the hopefully the images don't get bottle necked
    full_pool = []
    for card in all_cards:
        pair = {"english": card.english, "spanish": card.spanish}
        full_pool.append(pair)

    game_id = str(uuid.uuid4())
    games[game_id] = {
        "pairs": pairs,
        "full_pool": full_pool,
        "current_index": 0,
        "score": 0,
        "total": len(pairs),
        "translation_revealed": False,
        "game_mode": game_mode,
    }

    game_state = _build_flashcard_state(game_id)

    return {"game_id": game_id, 
            "state": game_state}

def reveal_translation(game_id):
    '''
    reveal the English translation

    :param game_id: game id
    '''
    game = games.get(game_id)
    if not game:
        return {"error": "Game not found."}

    game["translation_revealed"] = True
    game_state = _build_flashcard_state(game_id)
    return game_state

def handle_flashcard_click(game_id, chosen_english):
    '''
    handle the user clicking one of the available choices options

    :param game_id: game id
    :param chosen_english: the english word associated with the clicked options
    '''
    game = games.get(game_id)
    if not game:
        return {"error": "Game not found."}

    pairs = game["pairs"]
    current_index = game["current_index"]
    current_pair = pairs[current_index]

    # compare the words
    correct = False
    chosen_clean = chosen_english.strip().lower()
    correct_clean = current_pair["english"].strip().lower()
    if chosen_clean == correct_clean:
        correct = True

    # add point if right
    if correct:
        game["score"] += 1

    # always reveal the translation when a picture is clicked
    game["translation_revealed"] = True

    # next up
    game["current_index"] += 1

    # is the game over?
    if game["current_index"] >= game["total"]:
        finished = True
        next_state = None

    else:
        finished = False
        # build the next state if the game is not finished
        next_state = _build_flashcard_state(game_id)

    game_state = {
        "correct": correct,
        "correct_english": current_pair["english"],
        "finished": finished,
        "score": game["score"],
        "total": game["total"],
        "state": next_state,
    }

    return game_state

def get_flashcard_image(word):
    '''
    return an image path for the incoming word

    :param word: english word to generate an image for
    '''
    return _image_generation(word)

def _build_flashcard_state(game_id):
    '''
    handle building and sending the flashcard state to the frontend

    :param game_id: game id
    '''
    game = games.get(game_id)
    if not game:
        return {}

    pairs = game["pairs"]
    current_index = game["current_index"]
    total = game["total"]

    # is the game over?
    if current_index >= total:
        # return the state then
        finished = True
        finished_state = {
            "finished": True,
            "score": game["score"],
            "total": total,
            "current_index": current_index,
            "translation_revealed": False,
        }
        return finished_state
    else:
        finished = False

    current_pair = pairs[current_index]

    # make 3 random images from all the options
    # don't make a repeat of the correct answer
    other_pairs = []
    for temp in game["full_pool"]:
        if temp["english"] != current_pair["english"]:
            other_pairs.append(temp)
 
    random.shuffle(other_pairs)
    wrong_choices = other_pairs[:3]
 
    # 1 correct + 3 wrong, then shuffle so the correct one isn't always first
    choices = [current_pair] + wrong_choices
    random.shuffle(choices)
 
    # set up what choices are available
    choices_list = []
    for temp_choice in choices:
        choice = {"english": temp_choice["english"], 
                  "spanish": temp_choice["spanish"]}
        choices_list.append(choice)
 
    # if the translation is shown, show it
    if game["translation_revealed"]:
        english_translation = current_pair["english"]
    else:
        english_translation = None
 
    game_state = {
        "finished": False,
        "current_index": current_index,
        "total": total,
        "score": game["score"],
        "game_mode": game["game_mode"],
        "spanish_word": current_pair["spanish"],
        "correct_english": current_pair["english"],
        "translation_revealed": game["translation_revealed"],
        "english_translation": english_translation,
        "choices": choices_list,
    }
 
    return game_state


# shared functions for both game types
def _get_mimetype(image_path):
    '''
    return the correct mimetype for the image path based on its extension
    adapted from a stack overflow: https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
 
    :param image_path: path to the image file
    '''
    mimetype, _ = mimetypes.guess_type(image_path)
    if mimetype is None:
        mimetype = "image/png"
    return mimetype

def _open_file(key_word):
    try:
        base_path = ""
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = os.path.join(sys._MEIPASS, "minigames")
        else:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minigames")

        folders = [os.path.join(base_path, "images", "default-images"),
                   os.path.join(base_path, "images")]
        for eachFolder in folders:
            matches = glob.glob(os.path.join(eachFolder, f"{key_word}.*"))  # ← fix here
            if matches:
                return matches[0]
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def _get_keyword(word):
    '''
    clean up the word and get the main idea

    :param word: english word 
    '''

    # Strip punctuation markers like ¡ ! ¿ ? and trailing periods
    clean_word = re.sub(r'[¡¿!?.]', '', word).strip()

    # Remove bracketed expressions entirely, e.g. "[inf to feel like]"
    clean_word = re.sub(r'\[.*?\]', '', clean_word).strip()

    # Remove everything after a semicolon (alternative phrases)
    clean_word = clean_word.split(';')[0].strip()

    # Remove parenthetical expressions, including unclosed ones e.g. "(pragmatically: no more mate"
    clean_word = re.sub(r'\(.*?\)', '', clean_word).strip()
    clean_word = re.sub(r'\(.*$', '', clean_word).strip()  # unclosed paren

    # Remove quoted strings (they are examples, not alternatives)
    clean_word = re.sub(r'".*?"', '', clean_word).strip()

    # Take only the first alternative when separated by " / " or " \ "
    clean_word = re.split(r'\s*/\s*|\s*\\\s*', clean_word)[0].strip()

    # Remove everything after a comma
    clean_word = clean_word.split(',')[0].strip()

    # Collapse extra whitespace
    clean_word = re.sub(r'\s+', ' ', clean_word).strip()

    if not clean_word:
        # strip only ASCII special chars
        # i.e. handle the accented letters
        clean_word = re.sub(r'[^\w\s\'-]', '', word, flags=re.UNICODE).strip()

    # If still short and clean, return as-is
    if len(clean_word) <= 100:
        clean_word = clean_word.replace("/", "-")
        return clean_word

    # For very long results, extract the first non-filler word
    noneed_words = {"to", "a", "the", "of", "in", "on", "at", "for", "with", "by", "from"}
    words = clean_word.split()
    for eachWord in words:
        if eachWord.lower() not in noneed_words:
            clean_word = eachWord.replace("/", "-")
            return clean_word

    clean_word = words[0].replace("/", "-")
    return clean_word

def _image_generation(word):
    '''
    handle getting the default images
    handle getting the image from the offsite model
    handle if both models are rate limited
    save it locally

    :param word: english word 
    '''
    key_word = _get_keyword(word)

    # try to see if the image has already exsists
    file_created = _open_file(key_word)
    if file_created:
        return file_created, _get_mimetype(file_created)
    
    base_path = ""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # pyinstaller
        base_path = os.path.join(sys._MEIPASS, "minigames")
    else:
        # wsgi or local
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minigames")

    image_path = os.path.join(base_path, "images", f"{key_word}.png")

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
            return image_path, _get_mimetype(image_path)
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
        return image_path, _get_mimetype(image_path)
    except Exception as e:
        print(f"Cannot find an image for {word}: {e}")
        return None
