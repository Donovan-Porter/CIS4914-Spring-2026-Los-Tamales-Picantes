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
- [Transformers](https://pypi.org/project/transformers/) (text-to-text (t2t), and translation, models)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (Bundles source code into a single executable for ease of consumption)
- [PyAudio](https://pypi.org/project/PyAudio/) (Cross-platform IO)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (Sets environment variables from `.env` file)
- [Pillow](http://pypi.org/project/pillow/) (Imaging Library)


After installing Python, the requisite packages can be installed via the given `dependencies.bat`.
This is equivalent to `pip install <package1> <package2>...`, and `py download_model.py`.
Just the second can be run if you're dealing with an established python installation, but new repository files.

The LLM used as of *Jan 19, 2026*, is included in the folder `/model`.
It is the *Liquid AI*'s `LFM2-350M` model, which can be found on [HuggingFace](https://huggingface.co/LiquidAI/LFM2-350M).
The associated *lfm1* license is included in that directory.



##### Python Installation

The Python scripting language can be found [here](python.org/downloads/).
Follow the instructions there to install the most recent stable release.


## How to Run

### User

There are three methods to run this application.
1. Directly via Python.
    - Install Python, using the link from earlier.
        Ideally version 3.12 or later.
    - Run `tutor.bat`.
2. Download the executable.
    - You can look [here](https://mega.nz/file/Q29BXQwL#L9dkWO0-N50rksyZC91Co0-S-VbL6k-92CrEZjZhrEw) or [here](https://mega.nz/file/HPZBlaDD#eLTKKznsQK9LmDIui5WkjdzpjwEtCfEDTBxwqUd-Bzw) to find the executable for Windows.
    - It is a large file, and so may take some time to download.
    - There's no guarantee that the versions found here are up-to-date.
3. Create your own executable.
    - Install all the dependnecies (via running `dependencies.bat`).
    - Obtain the `.env` file, not included here.
    - Run `bundle.bat`.
    - Then, you can run `dist/tutor.exe`.
    - Keep in mind that PyInstaller may take some time.


### Developer

`tutor.bat` can be run on Windows to open a stand-alone application.
This is equivalent to `py tutor.py`.

For debugging mode, run `tutor_db.bat`.
This is equivalent to `py -m flask --app tutor run --debug`.
This requires you to navigate to the given IP address and port that is given in the opened CLI from inside a browser.


## Web Hosting

These are the steps to install the application on an Apache webserver running on Debian.
Anything in square brackets (`[` and `]`) is meant to be replaced with the actual value.

- Install Git.
- Clone Git repository to some path, I will be using `/srv/[app]/`.
    ```
    sudo git clone [repository] /srv/[app]
    ```
- Set up Python venv in `/srv/[app]/`.
    ```
    python3 -m venv /srv/[app]/[venv]
    ```
- Install dependencies via pip in the virtual environment. (The modules listed in dependencies, but minus `pyinstaller` and `pyaudio`, and plus `torch` and `sentencepiece`).
    ```
    source /srv/[app]/[venv]/bin/activate
    pip install Flask flaskwebgui transformers
    pip install python-dotenv
    pip install Pillow
    pip install torch
    pip install sentencepiece
    ```
- Download the Huggingface models.
    ```
    python3 /srv/[app]/download_model.py
    ```
- It may be necessary to install `sacremoses` via pip in the venv.
- Install Python package manager on the system via apt.
    ```
    sudo apt update
    sudo apt install python3-pip
    ```
- PyAudio needs to be installed on the system.
    ```
    sudo apt install python3-pyaudio
    ```
-  `/srv/[app]/[venv]/pyenv.cfg` needs to have `include-system-site-packages` set to `true`.
- Create `/srv/[app]/[app.wsgi]`.
    ```
    import sys
    import os

    sys.path.insert(0, '/srv/[app]')

    from [python file name] import [application variable name in file] as application
    ```
    (It may be necessary to include `/srv/[app]/__init__.py`.)
- Apache2 activation of necessary modules.
    ```
    a2enmod proxy
    a2enmod proxy_http
    a2enmod headers
    ```
- Change ownership to `www-data`.
    ```
    sudo chown -R www-data:www-data /srv/[app]
    ```
- Change the permissions of the root directory, as well as subdirectories and files.
    ```
    sudo chmod -R 644 /srv/[app]
    sudo chmod 755 /srv/[app]
    ```
- All parent directories need read and execute permissions for `www-data`, which should already be the case.
I mucked around and caused myself issues, though.
- Access error logs to see issues on load of the page.
By default on Debian for the Apache webserver they are found at `/var/log/apache2/error.log`.
You can see the last few lines with the following command.
    ```
    sudo tail /var/log/apache2/error.log
    ```
- Create Apache directory for wsgi script, probably in `/etc/apache2/apache2.conf`.
This is from the Flask documentation:
    ```
    <Directory /srv/[app]>
        WSGIProcessGroup [application]
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
    ```
- Create virtualhost in new `.conf` file in `/etc/apache2/sites-available/`.
This is from the Flask documentation, except the `python-home` variable in `WSGIDaemonProcess`.
    ```
    <VirtualHost *>
        ServerName [domain.com]

        WSGIDaemonProcess [application] python-home=/srv/[app]/[venv] user=www-data group=www-data threads=15
        ProxyPreserveHost On
        WSGIScriptAlias / /srv/[app]/[app.wsgi]
    </VirtualHost>
    ```
- This has dubious benefits.
Add aliases and directories for assets.
    ```
    <VirtualHost *>
        Alias /static [static folder]

        <Directory [static folder]>
            Require all granted
        </Directory>

        [...]
    </VirtualHost>
    ```
- You may need to add the data directories listed in `bundle.bat` as well in the previous step.
- This is optional.
Set `ServerName` and `ServerAlias`.
    ```
    <VirtualHost *>
        ServerName default
        ServerAlias *

        [...]
    </VirtualHost>
    ```
- Set up Apache reverse proxy file (I used `/etc/apache2/sites-available/000-default.conf`), and point it to the application port on localhost with `ProxyPass`.
    ```
    <VirtualHost *:80>

        <LocationMatch "/[app](?:/)?(.*)">
                RequestHeader set X-Forwarded-Prefix "/[app]"
                RequestHeader set X-Forwarded-Proto "http"
                ProxyPassMatch http://localhost:[port]/$1
                ProxyPassReverse http://localhost:[port]/$1
        </LocationMatch>

    </VirtualHost>
    ```
- So, altogether `/etc/apache2/sites-available/[app.conf]` looks something like this.
    ```
    <VirtualHost *:[port]>

        ServerName default
        ServerAlias *

        ProxyPreserveHost On
        RequestHeader set X-Forwarded-Prefix "/[app]"
        RequestHeader set X-Forwarded-Proto "http"

        WSGIDaemonProcess [app] python-home=/srv/[app]/[venv] user=www-data group=www-data

        Alias /static /srv/[app]/static
        Alias /templates /srv/[app]/templates
        Alias /model /srv/[app]/model

        <Directory /srv/[app]/static>
                Require all granted
        </Directory>

        <Directory /srv/[app]/templates>
                Require all granted
        </Directory>

        <Directory /srv/[app]/model>
                Require all granted
        </Directory>

        WSGIScriptAlias / /srv/[app]/[app.wsgi]

        <Directory /srv/[app]>
                WSGIProcessGroup [app]
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
                Order deny,allow
                Allow from all
        </Directory>

    </VirtualHost>
    ```
- Add the port from `/etc/apache2/sites-available/[app.conf]` to `/etc/apache2/ports.conf`.
- Git operations may change ownership, especially if using `sudo`, so it's recomended to do development in a different environment.
Additionally, creating a second folder to create the updated condition in, then simply pointing Apache to that at the end may reduce downtime during updates.
A script file to do the operations programmatically may be useful, as well.



## Future Development

- ~~Single executable to run~~
- ~~Flashcards.~~
- ~~Conjugation exercises.~~
- ~~Fill-in-the-blank exercises.~~
- ~~Spanish text-to-text chatting.~~
- Persistent learning profiles.
- Text-to-speech.
- Variable voice options.
- Speech-to-text.
- Custom PyTorch classifiers for vocal coaching.
- Hover-over dictionary lookup.
- ~~In-app translation.~~
- Targeted learning algorithms.
- Colloquialisms.
- Accents.
- Learning anchors in the form of geographical, geopolitical, and cultural, content.
- Significant gamification.
- Achievements and badges.
