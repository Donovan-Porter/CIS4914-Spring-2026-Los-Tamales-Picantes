set EAGER_IMPORT="true"
pyinstaller --onefile --add-data "local_users.db:." --add-data "static:static" --add-data "templates:templates" --add-data "model:model" --add-data "translation":"translation" --add-data "minigames:minigames" -y tutor.py
