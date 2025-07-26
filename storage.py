import json
import os
import hashlib

VOTES_FILE = "votes.json"

def load_data():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "hashes": [],
        "counts": {},
        "other": [],
        "lang": {}
    }

def save_data(data):
    with open(VOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_hash(user_id):
    salt = "safe_salt_123"  # Replace with your own random salt
    return hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()

def record_vote(data, user_hash, choice):
    if user_hash in data["hashes"]:
        return False
    data["hashes"].append(user_hash)
    data["counts"][choice] = data["counts"].get(choice, 0) + 1
    return True

def record_other(data, user_hash, custom_text):
    if user_hash in data["hashes"]:
        return False
    data["hashes"].append(user_hash)
    data["other"].append(custom_text)
    return True

def get_language(data, user_id):
    return data["lang"].get(str(user_id), "ru")

def toggle_language(data, user_id):
    uid = str(user_id)
    current = data["lang"].get(uid, "ru")
    new_lang = "en" if current == "ru" else "ru"
    data["lang"][uid] = new_lang
    return new_lang