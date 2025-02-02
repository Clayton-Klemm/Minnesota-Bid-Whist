# data_logger.py
import csv
import os
import datetime

LOG_FILE = "ml_decisions.csv"

def log_decision(decision_data):
    file_exists = os.path.isfile(LOG_FILE)
    fieldnames = [
        "timestamp", 
        "agent", 
        "phase", 
        "hand", 
        "current_trick", 
        "game_mode", 
        "bid_choice", 
        "selected_card", 
        "seen_cards", 
        "my_played_cards", 
        "global_played_cards",
        "tricks_played",
        "dealer_index"
    ]
    
    with open(LOG_FILE, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        decision_data["timestamp"] = datetime.datetime.now().isoformat()
        for field in fieldnames:
            if field not in decision_data:
                decision_data[field] = ""
        writer.writerow(decision_data)
