import os
import sys
import unicodedata
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
    # Return list of grammar courses (folders ending with -grammar).
    lr = os.path.join(base_path, 'static', 'learning-resources')
    if not os.path.isdir(lr):
        return []
    entries = [d for d in os.listdir(lr)
               if d.endswith('-grammar') and os.path.isdir(os.path.join(lr, d))]
    entries.sort()
    return entries

def generate_conjugation_story(pipe, grammar_phrases, title=None):
    try:
        phrases = [g.strip().rstrip('.!?') for g in grammar_phrases]
        result = []

        for phrase in phrases:

            user_prompt = (
                f'Write ONE simple Spanish sentence that begins with "{phrase}". '
                "The sentence must be 6–12 words total. "
                "Use present tense only. "
                "Keep it A1–A2 level. "
                "Make the grammar consistent with the subject. "
                "Do not list phrases. "
                "Write only the sentence."
            )

            messages = [{"role": "user", "content": user_prompt}]
            out = pipe(messages)

            sentence = out[0]['generated_text'][1]['content'].strip()
            sentence = sentence.replace("\n", " ").strip()

            # Keep only first sentence
            sentence = re.split(r'[.!?]', sentence)[0].strip()

            if not sentence:
                continue

            # Ensure it starts with the phrase (critical for stability)
            if not normalize_text(sentence).startswith(normalize_text(phrase)):
                continue

            # Enforce word count
            words = sentence.split()
            if len(words) < 6 or len(words) > 12:
                continue

            if not sentence.endswith("."):
                sentence += "."

            # Extract before/after (should always be before = "")
            phrase_norm = normalize_text(phrase)
            sentence_norm = normalize_text(sentence)

            match = re.search(phrase_norm, sentence_norm)
            if not match:
                continue

            start = match.start()
            end = match.end()

            before = sentence[:start]
            after = sentence[end:]

            result.append({
                "before": before,
                "word": phrase,
                "after": after
            })

        return result if result else None

    except Exception as e:
        print("ERROR in generate_conjugation_story:", e)
        return None