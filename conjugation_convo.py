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
        "Vosotros": "VosotrosCapy.png", # TODO: no images for vosotros/as rn
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
        if phrase.startswith(s + " "):
            return s
    return None

def fix_ser_identity(sentence, person_from, person_to):

    gender_map = {
        "Él": "masculine",
        "Ella": "feminine",
        "Ellos": "masculine",
        "Ellas": "feminine",
        "Nosotros": "masculine",
        "Nosotras": "feminine",
        "Vosotros": "masculine",
        "Vosotras": "feminine"
    }

    gender_to = gender_map.get(person_to)

    if not gender_to:
        return sentence

    article_map = {
        "masculine": {"la": "el", "una": "un", "las": "los"},
        "feminine": {"el": "la", "un": "una", "los": "las"}
    }

    def replace(match):
        article = match.group(1)

        if article in article_map[gender_to]:
            return match.group(0).replace(article, article_map[gender_to][article])

        return match.group(0)

    pattern = r'\b(es|son|somos|eres|soy|sois)\s+(el|la|los|las|un|una)\b'

    return re.sub(pattern, lambda m: m.group(1) + " " + article_map.get(gender_to, {}).get(m.group(2), m.group(2)), sentence)

def swap_indirect_pronouns(person_from, person_to, sentence):
    # define indirect pronouns based on the subject
    indirect_pronouns = {
        "Yo": "me",
        "Tú": "te",
        "Usted": "le",
        "Él": "le",
        "Ella": "le",
        "Nosotros": "nos",
        "Nosotras": "nos",
        "Vosotros": "os",
        "Vosotras": "os",
        "Ellos": "les",
        "Ellas": "les"
    }

    # get the indirect pronoun for each subject
    pronoun_from = indirect_pronouns.get(person_from, None)
    pronoun_to = indirect_pronouns.get(person_to, None)

    if pronoun_from and pronoun_to:
        sentence = re.sub(r'\b' + re.escape(pronoun_from) + r'\b', pronoun_to, sentence)
    
    return sentence

def fix_reflexive_infinitive(sentence, person_to):

    reflexive_map = {
        "Yo": "me",
        "Tú": "te",
        "Usted": "se",
        "Él": "se",
        "Ella": "se",
        "Nosotros": "nos",
        "Nosotras": "nos",
        "Vosotros": "os",
        "Vosotras": "os",
        "Ellos": "se",
        "Ellas": "se"
    }

    target_pronoun = reflexive_map.get(person_to)

    if not target_pronoun:
        return sentence

    # infinitive verbs with reflexive pronouns attached (e.g. "levantarse"), replace the pronoun with the correct one for the new subject
    pattern = r'\b(\w+(?:ar|er|ir))(me|te|se|nos|os)\b'

    def replace(match):
        verb = match.group(1)
        return verb + target_pronoun

    return re.sub(pattern, replace, sentence)

def generate_conjugation_exercise_from_list(pipe, grammar_list):

    conversation_mapping = {
        "Yo": "Tú",            # I → you
        "Tú": "Yo",            # you → me
        "Usted": "Yo",         # formal you → me
        "Él": "Él",            # he → he
        "Ella": "Ella",        # she → she
        "Nosotros": "Ustedes",  # we → you all (formal)
        "Nosotras": "Ustedes",  # we → you all (feminine, formal)
        "Ustedes": "Nosotros",  # you all (formal) → we (default masculine)
        "Ellos": "Ellos",      # they (m) → they (m)
        "Ellas": "Ellas",      # they (f) → they (f)
    }

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

        person_from = extract_subject(phrase_from)
        person_to = conversation_mapping.get(person_from)

        if not person_to:
            print(f"[DEBUG] No conversational mapping for {person_from}. Skipping.")
            continue

        # Find the phrase in grammar_phrases that starts with person_to
        phrase_to_candidates = [p for p in grammar_phrases if p.startswith(person_to + " ")]
        if not phrase_to_candidates:
            print(f"[DEBUG] No matching phrase_to for person_to {person_to}. Skipping.")
            continue

        phrase_to = phrase_to_candidates[0]  # choose first match

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


        if ":" in full_sentence or '"' in full_sentence:
            print(f"[DEBUG] Skipping sentence with invalid punctuation: {full_sentence}")
            continue

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

        # create question version of the original sentence
        words = full_sentence.rstrip(".").split()  # split into words

        if len(words) >= 2:
            # swap first two words
            words[0], words[1] = words[1], words[0]
            
            # capitalize first word (verb), lowercase second word (subject)
            words[0] = words[0].capitalize()
            words[1] = words[1].lower()
            
            sentence_question = " ".join(words)
            sentence_question = f"¿{sentence_question}?"
        else:
            # fallback if too short
            sentence_question = f"¿{full_sentence.rstrip('.')}?"

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

        print(f"[DEBUG] Extracted person_from: {person_from}")
        print(f"[DEBUG] Extracted person_to: {person_to}")

        if not person_from or not person_to:
            print("[DEBUG] Could not extract subject(s). Skipping.")
            continue

        sentence_changed = swap_indirect_pronouns(person_from, person_to, sentence_changed)
        sentence_changed = fix_ser_identity(sentence_changed, person_from, person_to)
        sentence_changed = fix_reflexive_infinitive(sentence_changed, person_to)

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
            "sentence_full": sentence_question,
            "sentence_blank": sentence_blank,
            "answer": phrase_to,
            "from": person_from,
            "to": person_to,
            "image_from": image_from,
            "image_to": image_to
        })


    print(f"[DEBUG] Total exercises generated: {len(exercises)}")

    return exercises