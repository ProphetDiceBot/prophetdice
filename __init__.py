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

def tune():
    nonce = get_nonce()
    api_key = "TCgWlc4bn25YPK6w6NFfyE1xDs1cMSvi"  # **REPLACE with your actual API key!**
    client = Mistral(api_key=api_key)
    game_history_path = "game_history.json"

    if not os.path.exists(game_history_path):
        current_game_history = pd.read_csv("current_game_history.csv")
        game_history = {
            "messages": [
                {"role": "system", "content": "You are an assistant helping with game outcome predictions on Primedice."},
                {"role": "user", "content": "Can you help me predict the outcome of the next game?"},
                {"role": "assistant", "content": "Let me analyze the recent game history to help with predictions."},
                {"role": "user", "content": f"Here is the recent game history: {current_game_history.to_string()}"},
                {"role": "assistant", "content": "Based on the recent outcomes, I will analyze the pattern to predict the next game."},
                {"role": "user", "content": "The last five results were 1, 0, 0, 1, 1.  What's your prediction?"},
                {"role": "assistant", "content": "Given the recent trend towards more 1s, I'd predict the next outcome is likely to be a 1, but it's still a gamble."},
                {"role": "user", "content": "The history shows a lot of alternating results. What do you think?"},
                {"role": "assistant", "content": "If there's a strong pattern of alternation, and the last result was a 0, I might predict a 1 for the next game. However, Primedice is based on random chance, so no prediction is guaranteed."},
            ],
            "game_history": [
                {"nonce": 0, "result": 0, "condition": 1},
                {"nonce": 1, "result": 1, "condition": 1},
                {"nonce": 2, "result": 0, "condition": 1},
                {"nonce": 3, "result": 1, "condition": 0},
                {"nonce": 4, "result": 1, "condition": 1},
                {"nonce": 5, "result": 1, "condition": 1},
                {"nonce": 6, "result": 0, "condition": 0},
                {"nonce": 7, "result": 1, "condition": 1}
            ]
        }

        with open(game_history_path, "w") as f:
            json.dump(game_history, f, indent=4)

    # Upload the JSON file (no change needed here)
    with open(game_history_path, "rb") as f:
        training_data = client.files.upload(file=f)
    print(f"Training data loaded successfully: {training_data.id}")

    # ... (The rest of your `tune` function, creating and starting the fine-tuning job, and getting the chat response.  No changes should be needed in this part if you use training_data.id as file_id.)
    created_jobs = client.fine_tuning.jobs.create(
        model="open-mistral-7b",  # Or the Mistral model you want to fine-tune
        training_files=[{"file_id": training_data.id, "weight": 1}], # Use the file ID from upload
        validation_files=[training_data.id],  # Use the file ID from upload
        hyperparameters={
            "training_steps": 10,  # Adjust as needed
            "learning_rate": 0.0001 # Adjust as needed
        },
        auto_start=False
    )

    client.fine_tuning.jobs.start(job_id=created_jobs.id)

    chat_response = client.chat.complete(
        model=created_jobs.fine_tuned_model,
        messages=[{"role": 'user', "content": f'nonce = {nonce} history = {current_game_history.to_string()} predict the next game'}]
    )
    print(chat_response)

tune()