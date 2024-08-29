import requests
import random

BASE_URL = "https://app.mochi.cards/api/"
SECRET_KEY = ""
DECK_ID = ""

def store_all_numbers():
    all_numbers = []
    req = {
        "limit": 100
    }
    more = True
    while more:
        res = requests.get(f'{BASE_URL}cards?deck-id={DECK_ID}',
                           params=req, auth=(SECRET_KEY, ""))
        deck = res.json()['docs']
        for card in deck:
            all_numbers.append(
                {'name': int(card['name'].replace(",", "")), 'new?': False if card['reviews'] else True})
        req['bookmark'] = res.json()['bookmark']
        if deck == []:
            more = False
    return all_numbers


def create_new_cards():
    all_numbers = store_all_numbers()

    def find_number():
        value = random.randint(10, 1_000_000_000)
        return f'{value:,}' if value not in all_numbers else find_number()

    if len([card for card in all_numbers if card['new?']]) > 10:
        return "Quiting"
    for _ in range(10):
        value = find_number()
        card = {
            "content": "",
            "deck-id": DECK_ID,
            "fields": {
                "name": {
                    "id": "name",
                    "value": value
                },
                "8T6pdCKh": {
                    "id": "8T6pdCKh",
                    "value": value.replace(",", "")
                }
            }
        }
        res = requests.post(f'{BASE_URL}cards/',
                            json=card, auth=(SECRET_KEY, ""))


create_new_cards()
