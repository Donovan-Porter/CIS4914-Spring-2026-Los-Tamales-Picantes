import os
import sys
import unicodedata
import random
import re

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def normalize_text(s):
    if s is None:
        return ""
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return s

def strip_article(s):
    s = s.strip()
    s_norm = normalize_text(s)
    articles = ['el ', 'la ', 'los ', 'las ', 'un ', 'una ']
    for a in articles:
        if s_norm.startswith(normalize_text(a)):
            return s[len(a):].strip()
    return s

def find_grammar_dirs():
    # return list of grammar courses (folders ending with -grammar).
    lr = os.path.join(base_path, 'static', 'learning-resources')
    if not os.path.isdir(lr):
        return []
    entries = [d for d in os.listdir(lr)
               if d.endswith('-grammar') and os.path.isdir(os.path.join(lr, d))]
    entries.sort()
    return entries

def clean_model_output(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # removes bold markdown
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # removes italic markdown
        
    text = text.replace('\n', ' ')  # replace newlines with space
    text = re.sub(r'\s+', ' ', text)  # replace multiple spaces with a single space
    
    # remove leading and trailing spaces
    text = text.strip()

    # check if the text contains more than one sentence, only take the first
    if '.' in text:
        text = text.split('.')[0].strip() + '.'

    return text

def subject_to_image(person):
    key = person.capitalize()

    mapping = {
        "Yo": "YoCapy.png",
        "Tú": "TuCapy.png",
        "Usted": "UstedCapy.png",
        "Él": "ElCapy.png",
        "Ella": "EllaCapy.png",
        "Nosotros": "NosotrosCapy.png",
        "Nosotras": "NosotrasCapy.png",
        "Vosotros": "VosotrosCapy.png",
        "Vosotras": "VosotrasCapy.png",
        "Ellos": "EllosCapy.png",
        "Ellas": "EllasCapy.png"
    }

    return mapping.get(key, "Default.png")

def extract_subject(phrase):
    subjects = [
        "Nosotros", "Nosotras",
        "Vosotros", "Vosotras",
        "Ellos", "Ellas",
        "Usted",
        "Ella", "Él",
        "Yo", "Tú"
    ]

    for s in subjects:
        if phrase.startswith(s + " "):  # ensure full word match
            return s
    return None

def swap_article_for_gender_change(sentence, person_from, person_to):
    """
    Swap the article (el/la, un/una) if there's a gender change between person_from and person_to.
    """
    gender_map = {
        "Yo": None, # no gender associated directly
        "Tú": None,
        "Usted": None,
        "Él": "masculine",
        "Ella": "feminine",
        "Nosotros": "masculine",
        "Nosotras": "feminine",
        "Vosotros": "masculine",
        "Vosotras": "feminine",
        "Ellos": "masculine",
        "Ellas": "feminine",
    }
    
    def get_gender(person):
        return gender_map.get(person, None)

    # get gender of both subjects
    gender_from = get_gender(person_from)
    gender_to = get_gender(person_to)

    # if gender changes
    if gender_from != gender_to:
        article_changes = {
            "el": "la", "la": "el",  # masculine/feminine singular
            "un": "una", "una": "un",  # masculine/feminine singular
            "los": "las", "las": "los",  # masculine/feminine plural
            "unos": "unas", "unas": "unos"  # masculine/feminine plural
        }

        for article_from, article_to in article_changes.items():
            sentence = re.sub(rf'\b{article_from}\b', article_to, sentence)
        
        adjective_changes = {
            "único": "única",
            "primer": "primera"
        }

        for adj_from, adj_to in adjective_changes.items():
            if gender_from == "masculine" and gender_to == "feminine":
                sentence = re.sub(rf'\b{adj_from}\b', adj_to, sentence)
            elif gender_from == "feminine" and gender_to == "masculine":
                sentence = re.sub(rf'\b{adj_to}\b', adj_from, sentence)
        
    return sentence

def swap_indirect_pronouns(person_from, person_to, sentence):
    # define indirect pronouns based on the subject
    indirect_pronouns = {
        "Yo": "me",        # Yo -> me
        "Tú": "te",        # Tú -> te
        "Usted": "le",     # Usted -> le
        "Él": "le",        # Él -> le
        "Ella": "le",      # Ella -> le
        "Nosotros": "nos", # Nosotros -> nos
        "Nosotras": "nos", # Nosotras -> nos
        "Vosotros": "os",  # Vosotros -> os
        "Vosotras": "os",  # Vosotras -> os
        "Ellos": "les",    # Ellos -> les
        "Ellas": "les"     # Ellas -> les
    }

    # get the indirect pronoun for each subject
    pronoun_from = indirect_pronouns.get(person_from, None)
    pronoun_to = indirect_pronouns.get(person_to, None)

    if pronoun_from and pronoun_to:
        sentence = re.sub(r'\b' + re.escape(pronoun_from) + r'\b', pronoun_to, sentence)
    
    return sentence

def generate_conjugation_exercise_from_list(pipe, grammar_list):

    exercises = []

    grammar_phrases = [
        item.strip() if isinstance(item, str)
        else item.get('derivative', '').strip()
        for item in grammar_list
    ]

    print("\n[DEBUG] Normalized grammar phrases:")
    for g in grammar_phrases:
        print("   -", g)

    for phrase_from in grammar_phrases:

        print("\n----------------------------------------")
        print(f"[DEBUG] Starting new exercise")
        print(f"[DEBUG] phrase_from: {phrase_from}")

        possible_targets = [p for p in grammar_phrases if p != phrase_from]

        if not possible_targets:
            print("[DEBUG] No possible targets. Skipping.")
            continue

        phrase_to = random.choice(possible_targets)

        print(f"[DEBUG] phrase_to selected: {phrase_to}")

        prompt = (
            f"Escribe SÓLO una oración que simple use EXACTAMENTE la frase '{phrase_from}'. "
            "No cambies el verbo ni el tiempo. Incluye un complemento."
        )

        print(f"[DEBUG] Prompt sent to model: {prompt}")

        out = pipe([{"role": "user", "content": prompt}])

        full_sentence = clean_model_output(
            out[0]['generated_text'][1]['content'].strip()
        )

        # common LLM generated mistake sentences to skip
        if full_sentence == "Yo soy yo." or full_sentence == "Yo soy tú.":
            print(f"[DEBUG] Skipping invalid sentence generation for phrase: {phrase_from}")
            continue

        print(f"[DEBUG] Model generated sentence: {full_sentence}")

        # exact match
        if not re.search(rf'\b{re.escape(phrase_from)}\b', full_sentence):
            print("[DEBUG] phrase_from NOT found exactly in sentence. Skipping.")
            continue

        print("[DEBUG] phrase_from found successfully.")

        # replace subject phrase
        sentence_changed = re.sub(
            rf'\b{re.escape(phrase_from)}\b',
            phrase_to,
            full_sentence,
            count=1
        )

        print(f"[DEBUG] Sentence after replacement: {sentence_changed}")

        if not re.search(rf'\b{re.escape(phrase_to)}\b', sentence_changed):
            print("[DEBUG] phrase_to NOT found after replacement. Skipping.")
            continue

        print("[DEBUG] phrase_to confirmed in changed sentence.")

        # extract subjects
        person_from = extract_subject(phrase_from)
        person_to = extract_subject(phrase_to)

        print(f"[DEBUG] Extracted person_from: {person_from}")
        print(f"[DEBUG] Extracted person_to: {person_to}")

        if not person_from or not person_to:
            print("[DEBUG] Could not extract subject(s). Skipping.")
            continue

        sentence_changed = swap_indirect_pronouns(person_from, person_to, sentence_changed)
        sentence_changed = swap_article_for_gender_change(sentence_changed, person_from, person_to)

        print(f"[DEBUG] Sentence after gender-based article swap: {sentence_changed}")

        # create blank
        sentence_blank = re.sub(
            rf'\b{re.escape(phrase_to)}\b',
            "_______",
            sentence_changed,
            count=1
        )

        print(f"[DEBUG] Sentence with blank: {sentence_blank}")

        image_from = f"/static/images/{subject_to_image(person_from)}"
        image_to = f"/static/images/{subject_to_image(person_to)}"

        print(f"[DEBUG] image_from path: {image_from}")
        print(f"[DEBUG] image_to path: {image_to}")

        exercises.append({
            "sentence_full": full_sentence,
            "sentence_blank": sentence_blank,
            "answer": phrase_to,
            "from": person_from,
            "to": person_to,
            "image_from": image_from,
            "image_to": image_to
        })


    print(f"[DEBUG] Total exercises generated: {len(exercises)}")

    return exercises