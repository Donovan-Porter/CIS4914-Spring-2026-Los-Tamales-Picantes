# Spanish Tutor, Chatbot, and Voice Coach

## Synopsis

This is a Spanish learning application.
It utilizes Python, and hypertext markup language (HTML) via Flask, for the graphical user interface (GUI).
Ollama provides text-to-text chatting capability.


## Installation

### Dependencies

- Python (scripting language); 3.12 or newer.
- Flask (Python package, web development)
- Flask Web GUI (Python package, stand-alone application interfaces based on Flask); requires Python 3.12 or newer.
- Ollama (Python package, text-to-text large-language model (LLM))
- PyIntaller (Bundles source code into a single executable for ease of consumption)
<!--> - Psychopy-Whisper (Python package, speech-to-text) <-->
<!--> - Vosk (Python package, speech-to-text) <-->
<!--> - ffmpeg (Python package, audio file manipulation) <-->

After installing Python, the requisitepackages can be installed via the given `dependencies.bat`.
This is equivalent to `pip install <package1> <package2>...`.

#### Python Installation

To install the Python scripting language, go to `python.org/downloads/` in a browser.
Follow the instructions to install the most recent stable release.


## How to Run

If PyInstaller has been run, and you're on Windows, then simply double-click dist/tutor/tutor.exe.

Otherwise, `tutor.bat` can be run on Windows to open a stand-alone application.
This is equivalent to `py tutor.py`.

For debugging mode, run `tutor_db.bat`.
This is equivalent to `py -m flask --app tutor run --debug`.
This requires you to navigate to the given IP address and port that is given in the opened CLI from inside a browser.


## Future Development

- ~~Single executable to run~~
- Spanish text-to-text chatting.
- Persistent learning profiles.
- Varied learning modalities (fill-in-the-blank, grammar exercises, flashcards, etc)
- Text-to-speech.
- Variable voice options.
- Speech-to-text.
- Custom PyTorch classifiers for vocal coaching.
- Hover-over dictionary lookup.
- Targeted learning algorithms.
- Slang.
- Accents.
- Learning anchors in the form of geographical, geopolitical, and cultural, content.
