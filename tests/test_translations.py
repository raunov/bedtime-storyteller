import json
import os

TRANSLATIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations.json")
REQUIRED_KEYS = ["title", "story_settings"]


def test_translation_keys_present():
    with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for lang, translations in data.items():
        for key in REQUIRED_KEYS:
            assert key in translations, f"Missing '{key}' for language '{lang}'"


