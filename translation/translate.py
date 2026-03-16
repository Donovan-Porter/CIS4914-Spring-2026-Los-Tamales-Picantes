
def GetModels() :

    from transformers import pipeline
    from transformers import MarianMTModel, MarianTokenizer
    import os, sys

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    model_dir = os.path.join(base_path, "en-es")
    en_es_tokenizer = MarianTokenizer.from_pretrained(model_dir)
    en_es_model = MarianMTModel.from_pretrained(model_dir)

    model_dir = os.path.join(base_path, "es-en")
    es_en_tokenizer = MarianTokenizer.from_pretrained(model_dir)
    es_en_model = MarianMTModel.from_pretrained(model_dir)

    return ((en_es_tokenizer, en_es_model), (es_en_tokenizer, es_en_model))


# Google-generated code.
def Translate(text, tokenizer, model):

    # 3. Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    
    # 4. Generate translation
    translated_tokens = model.generate(**inputs)
    
    # 5. Decode the output tokens back to text
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

