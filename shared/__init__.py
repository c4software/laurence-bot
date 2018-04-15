import threading

shared = {}


def get_data(key=None):
    ident = threading.get_ident()
    if ident in shared:
        if key:
            return shared[ident][key]
        else:
            return shared[ident]


def save_data(key, data):
    ident = threading.get_ident()
    if ident not in shared:
        shared[ident] = {}

    shared[ident][key] = data


def clean_data():
    ident = threading.get_ident()
    del shared[ident]
