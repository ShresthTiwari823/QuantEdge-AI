import json
import os

WATCHLIST_FILE = "watchlist.json"


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []

    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)


def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_to_watchlist(symbol):
    watchlist = load_watchlist()

    if symbol not in watchlist:
        watchlist.append(symbol)
        save_watchlist(watchlist)


def remove_from_watchlist(symbol):
    watchlist = load_watchlist()

    if symbol in watchlist:
        watchlist.remove(symbol)
        save_watchlist(watchlist)


def get_watchlist():
    return load_watchlist()