# Use a pipeline as a high-level helper
from transformers import pipeline
import os

pipe = pipeline("text-generation", model=os.path.join(os.getcwd(), "model"))
messages = [
    {"role": "user", "content": "Hola, como estas?"},
]

out = pipe(messages)
print(out[0]['generated_text'][1]['content'])