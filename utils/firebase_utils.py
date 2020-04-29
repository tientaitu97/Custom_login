import os
from django.conf import settings

import firebase_admin
from firebase_admin import credentials

default_app = None


def get_default_app():
    global default_app
    if default_app is None:
        cre = credentials.Certificate(os.path.join(settings.BASE_DIR, 'firebase', 'evchat_prod_firebase_adminsdk.json'))
        default_app = firebase_admin.initialize_app(credential=cre)
    return default_app

def setData(ref, data, status):
    data['status'] = status
    ref.set(data)