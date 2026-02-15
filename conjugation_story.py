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

# Generate a story using a list of Spanish verbs/grammar items. Each item in grammar_list should be a string (e.g., 'hablar - present yo').
def generate_conjugation_story(pipe, grammar_group_examples, title=None):

    try:
        grammar_str = ", ".join(grammar_group_examples)
        user_prompt = (
            f"Write a short story in Spanish using the following sentences/phrases: {grammar_str}. "
            "Keep it simple (A1–A2 level), present tense, 6–10 words per sentence. "
            "Use the exact sentences provided. "
            "Do not translate. Make the story coherent and natural."
        )

        messages = [{"role": "user", "content": user_prompt}]
        out = pipe(messages)
        story_text = out[0]['generated_text'][1]['content'].strip()

        # split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', story_text)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        result = []
        used_sentences = set()

        for g in grammar_group_examples:
            g_norm = normalize_text(g)
            found_sentence = None

            # find an unused sentence containing the grammar example
            for s in clean_sentences:
                if s in used_sentences:
                    continue
                if normalize_text(s).find(g_norm) != -1:
                    found_sentence = s
                    used_sentences.add(s)
                    break

            # skip if LLM didn't generate sentence with the grammar example
            if not found_sentence:
                continue

            match = re.search(g_norm, normalize_text(found_sentence))
            if not match:
                continue

            start = match.start()
            end = match.end()

            before = found_sentence[:start]
            after = found_sentence[end:]

            result.append({
                "before": before,
                "word": g,
                "after": after
            })

        return result

    except Exception as e:
        print("ERROR in generate_story_with_model:", e)
        return None
