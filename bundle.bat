set EAGER_IMPORT="true"
pyinstaller --onefile --add-data "local_users.db:." --add-data "static:static" --add-data "templates:templates" --add-data "model:model" -y tutor.py