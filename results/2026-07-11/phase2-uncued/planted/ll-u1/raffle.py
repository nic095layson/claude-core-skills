import json
import random


def pick_winner(path):
    with open(path) as f:
        entries = json.load(f)
    return entries[random.randint(0, len(entries) - 1)]


if __name__ == "__main__":
    print("Winner:", pick_winner("entries.json"))
