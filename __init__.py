import os
from mistralai import Mistral
import json
import pandas as pd

def get_nonce():
    if not os.path.exists('current_game_history.csv'):
        raise FileNotFoundError("The file 'current_game_history.csv' does not exist.")

    with open('current_game_history.csv', 'r') as file:
        data = file.readlines()
        nonce = len(data)
        return nonce

