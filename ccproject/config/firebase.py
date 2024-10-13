# firebase.py

import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyA36ZcO_8j-ncsqxgTsBcj6_smGeVWp07w",
    "authDomain": "cold-mail-gen-profiles.firebaseapp.com",
    "databaseURL": "https://cold-mail-gen-profiles-default-rtdb.firebaseio.com/",  # Use this as the databaseURL
    "projectId": "cold-mail-gen-profiles",
    "storageBucket": "cold-mail-gen-profiles.appspot.com",
    "messagingSenderId": "854289840882",
    "appId": "1:854289840882:web:f32aeaf2db723768a82e6b",
    "measurementId": "G-RMMESGES5M"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
