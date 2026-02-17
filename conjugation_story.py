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
    # return list of grammar courses (folders ending with -grammar).
    lr = os.path.join(base_path, 'static', 'learning-resources')
    if not os.path.isdir(lr):
        return []
    entries = [d for d in os.listdir(lr)
               if d.endswith('-grammar') and os.path.isdir(os.path.join(lr, d))]
    entries.sort()
    return entries

def generate_conjugation_story(pipe, grammar_phrases, title=None):
    try:
        # remove trailing punctuation
        phrases = [g.strip().rstrip('.!?') for g in grammar_phrases]
        phrase_str = ", ".join(phrases)

        user_prompt = (
            f"Write ONE simple Spanish sentence for EACH of the following phrases: {phrase_str}. "
            "Keep sentences 6–12 words. "
            "A1–A2 level Spanish. "
            "Include a second simple action joined with 'y'. "
            "Write only the sentences."
        )

        messages = [{"role": "user", "content": user_prompt}]
        out = pipe(messages)

        story_text = out[0]['generated_text'][1]['content'].strip()
        story_text = story_text.replace("\n", " ")

        sentences = re.split(r'(?<=[.!?])\s+', story_text)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        result = []
        used_sentences = set()

        for phrase in phrases:
            phrase_norm = normalize_text(phrase)
            found_sentence = None

            # find unused sentence that starts with phrase
            for s in clean_sentences:
                if s in used_sentences:
                    continue
                if normalize_text(s).startswith(phrase_norm):
                    found_sentence = s
                    used_sentences.add(s)
                    break

            if not found_sentence:
                continue

            match = re.search(phrase_norm, normalize_text(found_sentence))
            if not match:
                continue

            start = match.start()
            end = match.end()

            before = found_sentence[:start]
            after = found_sentence[end:]

            result.append({
                "before": before,
                "word": phrase,
                "after": after
            })

        return result if result else None

    except Exception as e:
        print("ERROR in generate_conjugation_story:", e)
        return None
