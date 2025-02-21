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
        "previous_bids",  # Bidding phase
        "bid_choice",     # Bidding phase
        "selected_card",
        "current_trick",  # Playing phase
        "game_mode",      # Playing phase
        "bids",           # Playing phase
        "my_played_cards",
        "global_played_cards",
        "tricks_played",
        "tricks_won",     # Playing phase
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