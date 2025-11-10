from firebase_admin import credentials, initialize_app
import firebase_admin
from django.conf import settings

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL)
        initialize_app(cred)
