import json
import time
import random
import csv
from datetime import datetime
import os

# Paths to configuration files
DEFAULT_CONFIG_PATH = "config/default-config.json"
CUSTOM_CONFIG_PATH = "config/custom-config.json"
TRADE_HISTORY_PATH = "results/trade-history.csv"


def load_config(file_path):
    """Load the configuration file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file {file_path} not found.")
        return None

def save_trade_history(trade_data):
    """Save trade results to the trade history CSV file."""
    file_exists = os.path.exists(TRADE_HISTORY_PATH)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(TRADE_HISTORY_PATH), exist_ok=True)

    # Open the file in append mode
    with open(TRADE_HISTORY_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers if the file is new
        if not file_exists:
            writer.writerow(["Timestamp", "Trade", "Outcome", "Stake", "Profit/Loss"])

        # Write the trade data
        writer.writerow(trade_data)

def simulate_trade():
    """Simulate a trade outcome (win or lose) with a 50% probability."""
    return random.choice(["win", "lose"])

def run_trading_bot(config):
    """Run the trading bot using the provided configuration."""
    stake = config["initial_stake"]
    profit = 0
    loss = 0
    stake_index = 0
    trade_count = 0

    print("Starting trading bot...")
    while profit < config["take_profit"] and loss < config["stop_loss"]:
        trade_count += 1
        trade_outcome = simulate_trade()

        if trade_outcome == "win":
            profit += stake
            print(f"Trade {trade_count}: WIN | Stake: {stake:.2f} | Profit: {profit:.2f}")
            save_trade_history([
                datetime.now().isoformat(),
                trade_count,
                "WIN",
                stake,
                stake
            ])
            stake = config["initial_stake"]  # Reset stake
            stake_index = 0
        else:
            loss += stake
            print(f"Trade {trade_count}: LOSE | Stake: {stake:.2f} | Loss: {loss:.2f}")
            save_trade_history([
                datetime.now().isoformat(),
                trade_count,
                "LOSE",
                stake,
                -stake
            ])
            # Adjust stake using martingale strategy
            stake_index = min(stake_index + 1, len(config["stake_list"]) - 1)
            stake = config["stake_list"][stake_index] * config["martingale_multiplier"]

    if profit >= config["take_profit"]:
        print("Take profit target reached!")
    elif loss >= config["stop_loss"]:
        print("Stop loss limit reached!")

if __name__ == "__main__":
    # Load custom or default configuration
    config = load_config(CUSTOM_CONFIG_PATH) or load_config(DEFAULT_CONFIG_PATH)

    if not config:
        print("Failed to load configuration. Exiting.")
    else:
        # Run the trading bot
        run_trading_bot(config)
