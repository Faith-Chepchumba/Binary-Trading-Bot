import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to the trade history CSV file
TRADE_HISTORY_PATH = "results/trade-history.csv"


def load_trade_history():
    """Load the trade history from the CSV file."""
    if not os.path.exists(TRADE_HISTORY_PATH):
        print(f"Trade history file not found at {TRADE_HISTORY_PATH}.")
        return None
    return pd.read_csv(TRADE_HISTORY_PATH)


def analyze_trade_history(data):
    """Analyze the trade history for performance metrics."""
    if data is None or data.empty:
        print("No data available for analysis.")
        return

    print("Analyzing trade history...")

    # Calculate metrics
    total_trades = len(data)
    total_wins = len(data[data["Outcome"] == "WIN"])
    total_losses = len(data[data["Outcome"] == "LOSE"])
    total_profit = data["Profit/Loss"].sum()
    win_rate = (total_wins / total_trades) * 100 if total_trades > 0 else 0
    loss_rate = (total_losses / total_trades) * 100 if total_trades > 0 else 0

    # Display metrics
    print("\nTrade Performance Metrics:")
    print(f"Total Trades: {total_trades}")
    print(f"Total Wins: {total_wins}")
    print(f"Total Losses: {total_losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Loss Rate: {loss_rate:.2f}%")
    print(f"Total Profit/Loss: {total_profit:.2f}")

    return {
        "total_trades": total_trades,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "total_profit": total_profit,
    }


def plot_cumulative_profit(data):
    """Plot the cumulative profit/loss over time."""
    if data is None or data.empty:
        print("No data available for plotting.")
        return

    # Calculate cumulative profit/loss
    data["Cumulative Profit/Loss"] = data["Profit/Loss"].cumsum()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(data["Timestamp"], data["Cumulative Profit/Loss"], marker="o")
    plt.title("Cumulative Profit/Loss Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Cumulative Profit/Loss")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load the trade history
    trade_data = load_trade_history()

    if trade_data is not None:
        # Analyze the trade history
        metrics = analyze_trade_history(trade_data)

        # Plot cumulative profit/loss
        plot_cumulative_profit(trade_data)
