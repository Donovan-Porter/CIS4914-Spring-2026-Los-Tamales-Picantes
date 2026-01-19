# Spanish Tutor, Chatbot, and Voice Coach

## Synopsis

This is a Spanish learning application created as a senior project for the Spring 2026 semester for the group *Los Tamales Picantes*.
It utilizes Python, and hypertext markup language (HTML) via Flask, for the graphical user interface (GUI).


## Installation

### Dependencies

#### User

None.


#### Developer

- [Python](https://python.org) (scripting language); 3.12 or newer.
- [Flask](https://pypi.org/project/Flask/) (Python package, web development)
- [Flask Web GUI](https://pypi.org/project/flaskwebgui/) (Python package, stand-alone application interfaces based on Flask); requires Python 3.12 or newer.
- ~~[Ollama](https://pypi.org/project/ollama/) (Python package, text-to-text large-language model (LLM))~~
- [Transformers](https://pypi.org/project/transformers/) (text-to-text (t2t) model used now instead of Ollama)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (Bundles source code into a single executable for ease of consumption)

<!--> - Psychopy-Whisper (Python package, speech-to-text) <-->
<!--> - Vosk (Python package, speech-to-text) <-->
<!--> - ffmpeg (Python package, audio file manipulation) <-->

After installing Python, the requisite packages can be installed via the given `dependencies.bat`.
This is equivalent to `pip install <package1> <package2>...`.

The LLM used as of Jan 19, 2026, is included in the folder `/model`.
It is the *Liquid AI*'s `LFM2-350M` model, which can be found on [HuggingFace](https://huggingface.co/LiquidAI/LFM2-350M).
The associated *lfm1* license is included in that directory.


##### Python Installation

The Python scripting language can be installed [here](python.org/downloads/).
Follow the instructions to install the most recent stable release.


## How to Run

### User

~~If PyInstaller was run before the code was pulled, and you're on Windows, then you should only need to run `dist/tutor/tutor.exe`.~~
End users should not be here; please refer to this [link](https://mega.nz/folder/ovMjlajJ#4AlZ0oFrY9M3Zy3VLrcEjg) to find the executable for Windows, as I've added the output of PyInstaller to the git ignore-list.


### Developer

`tutor.bat` can be run on Windows to open a stand-alone application.
This is equivalent to `py tutor.py`.

For debugging mode, run `tutor_db.bat`.
This is equivalent to `py -m flask --app tutor run --debug`.
This requires you to navigate to the given IP address and port that is given in the opened CLI from inside a browser.


## Future Development

- ~~Single executable to run~~
- Flashcards.
- Conjugation exercises.
- Fill-in-the-blank exercises.
- Spanish text-to-text chatting.
- Persistent learning profiles.
- Text-to-speech.
- Variable voice options.
- Speech-to-text.
- Custom PyTorch classifiers for vocal coaching.
- Hover-over dictionary lookup.
- In-app translation.
- Targeted learning algorithms.
- Colloquialisms.
- Accents.
- Learning anchors in the form of geographical, geopolitical, and cultural, content.
