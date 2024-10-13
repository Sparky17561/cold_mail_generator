# firebase_admin_setup.py
import firebase_admin
from firebase_admin import credentials, db

# Use the application default credentials
cred = credentials.Certificate("config/cold-mail-gen-profiles-firebase-adminsdk-v5jlq-70f1568797.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cold-mail-gen-profiles-default-rtdb.firebaseio.com/'
})

# Now you can use db to access your Firebase database
