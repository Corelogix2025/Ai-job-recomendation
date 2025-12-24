import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ai-job-ba0f5-default-rtdb.firebaseio.com/"
})



def get_jobs():
    ref = db.reference("jobs")
    return ref.get()
