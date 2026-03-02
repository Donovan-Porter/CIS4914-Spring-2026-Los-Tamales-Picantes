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
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text) # Removes bold markdown
    text = re.sub(r'\*([^*]+)\*', r'\1', text) # Removes italic markdown
        
    text = text.replace('\n', ' ')  # Replace newlines with space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    
    # Remove leading and trailing spaces
    text = text.strip()  
    return text

def subject_to_image(person):
    # Normalize capitalization
    key = person.capitalize()

    # Map plural feminine/masculine to shared images if needed
    mapping = {
        "Yo": "Yo.png",
        "Tú": "Tu.png",
        "Usted": "Usted.png",
        "Él": "El.png",
        "Ella": "Ella.png",
        "Nosotros": "Nosotros.png",
        "Nosotras": "Nosotras.png",
        "Vosotros": "Vosotros.png",
        "Vosotras": "Vosotras.png",
        "Ellos": "Ellos.png",
        "Ellas": "Ellas.png"
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
            f"Escribe SÓLO una oración que use EXACTAMENTE la frase '{phrase_from}'. "
            "No cambies el verbo ni el tiempo. Incluye un complemento."
        )

        print(f"[DEBUG] Prompt sent to model: {prompt}")

        out = pipe([{"role": "user", "content": prompt}])

        full_sentence = clean_model_output(
            out[0]['generated_text'][1]['content'].strip()
        )

        print(f"[DEBUG] Model generated sentence: {full_sentence}")

        # Ensure exact match
        if not re.search(rf'\b{re.escape(phrase_from)}\b', full_sentence):
            print("[DEBUG] phrase_from NOT found exactly in sentence. Skipping.")
            continue

        print("[DEBUG] phrase_from found successfully.")

        # Replace subject phrase
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

        # Extract subjects
        person_from = extract_subject(phrase_from)
        person_to = extract_subject(phrase_to)

        print(f"[DEBUG] Extracted person_from: {person_from}")
        print(f"[DEBUG] Extracted person_to: {person_to}")

        if not person_from or not person_to:
            print("[DEBUG] Could not extract subject(s). Skipping.")
            continue

        # Create blank
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