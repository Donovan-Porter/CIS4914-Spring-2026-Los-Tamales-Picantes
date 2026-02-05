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

def find_vocab_dirs():
    lr = os.path.join(base_path, 'static', 'learning-resources')
    if not os.path.isdir(lr):
        return []
    entries = [d for d in os.listdir(lr) if d.endswith('-vocab') and os.path.isdir(os.path.join(lr, d))]
    entries.sort()
    return entries

# using language model to generate a short story with given vocab list
def generate_story_with_model(pipe, vocab_list, title=None):
    try:
        vocab_str = ", ".join(vocab_list)
        user_prompt = (
            f"Write a short story using the following Spanish vocab words: {vocab_str}. "
            "Keep it simple (A1–A2 level), present tense, 6–10 words per sentence. "
            "Do not translate the words; use them as written. "
            "The story should be coherent and natural."
        )

        messages = [{"role": "user", "content": user_prompt}]
        out = pipe(messages)
        story_text = out[0]['generated_text'][1]['content'].strip()

        sentences = re.split(r'(?<=[.!?])\s+', story_text)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        result = []
        used_sentences = set()

        for w in vocab_list:
            w_norm = normalize_text(strip_article(w))
            found_sentence = None

            # find an unused sentence containing the vocab word
            for s in clean_sentences:
                if s in used_sentences:
                    continue
                if normalize_text(s).find(w_norm) != -1:
                    found_sentence = s
                    used_sentences.add(s)
                    break

            # TODO: sometimes LLM doesn't generate correctly, so if vocab word not found in any sentence, skip it
            if not found_sentence:
                continue

            s_norm = normalize_text(found_sentence)
            idx = s_norm.find(w_norm)

            if idx != -1:
                orig_idx = found_sentence.lower().find(w_norm)
                before = found_sentence[:orig_idx].rstrip()

                if before.endswith(("el", "la", "los", "las", "un", "una")):
                    before_words = before.split()
                    if before_words[-1] in ["el", "la", "los", "las", "un", "una"]:
                        before = " ".join(before_words[:-1]) + " "

                after = found_sentence[orig_idx + len(w):].lstrip()
            else:
                before, after = found_sentence, ""

            result.append({
                "before": before,
                "word": strip_article(w),
                "after": after
            })

        return result

    except Exception as e:
        print("ERROR in generate_story_with_model:", e)
        return None
