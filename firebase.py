import pyrebase
from dotenv import load_dotenv
import os
load_dotenv()

#pip install pyrebase4
#https://www.youtube.com/watch?v=HltzFtn9f1c

class firebase_handler:
        def __init__(self):
            self.config = {
                            'apiKey': os.getenv("FIREBASE_API_KEY"),
                            'authDomain': "los-tamales-picantes.firebaseapp.com",
                            'projectId': "los-tamales-picantes",
                            'storageBucket': "los-tamales-picantes.firebasestorage.app",
                            'messagingSenderId': os.getenv("FIREBASE_SENDERID"),
                            'appId': os.getenv("FIREBASE_APPID"),
                            'databaseURL': os.getenv("FIREBASE_DB_URL")
                          }
            self.firebase = pyrebase.initialize_app(self.config)
            self.auth = self.firebase.auth()
            self.db = self.firebase.database()
            
            
        def sign_up_user(self, email, password):
          user = self.auth.create_user_with_email_and_password(email, password)
          uid = user["localId"]
          self.db.child('picanteUsers').child(uid).set({
            'points': 0,
            'email': email
          })
          
        def login_user(self, email, password):
          user = self.auth.sign_in_with_email_and_password(email, password)
          return user
        
        
        def get_points(self, uid):
          info = self.db.child('picanteUsers').child(uid).get().val()
          if info:
            return info.get("points", 0)