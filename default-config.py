import json
import os

# Path to the default configuration file
DEFAULT_CONFIG_PATH = "config/default-config.json"

# Default configuration template
DEFAULT_CONFIG = {
    "initial_stake": 0.35,
    "stake_list": [0.35, 0.43, 0.85, 1.74, 3.55, 7.3, 15, 31, 65, 130, 260],
    "martingale_multiplier": 2,
    "take_profit": 20,
    "stop_loss": 20,
    "ticks": 1
}


def load_default_config():
    """Load the default configuration file."""
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        print(f"Default configuration file not found. Creating a new one at {DEFAULT_CONFIG_PATH}.")
        save_default_config(DEFAULT_CONFIG)  # Create a default config if missing
    with open(DEFAULT_CONFIG_PATH, "r") as file:
        config = json.load(file)
    print("Default configuration loaded successfully.")
    return config


def save_default_config(config):
    """Save the default configuration file."""
    os.makedirs(os.path.dirname(DEFAULT_CONFIG_PATH), exist_ok=True)  # Ensure the directory exists
    with open(DEFAULT_CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
    print(f"Default configuration saved to {DEFAULT_CONFIG_PATH}.")


def update_default_config(config, updates):
    """Update the default configuration with new values."""
    for key, value in updates.items():
        if key in config:
            config[key] = value
            print(f"Updated '{key}' to {value}.")
        else:
            print(f"Key '{key}' not found in the configuration.")
    save_default_config(config)
    return config


def validate_config(config):
    """Validate the configuration for required fields and correct values."""
    errors = []
    # Check required fields
    required_fields = ["initial_stake", "stake_list", "martingale_multiplier", "take_profit", "stop_loss", "ticks"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")

    # Validate individual fields
    if "initial_stake" in config and config["initial_stake"] <= 0:
        errors.append("initial_stake must be greater than 0.")

    if "stake_list" in config and not all(s > 0 for s in config["stake_list"]):
        errors.append("All values in stake_list must be greater than 0.")

    if "martingale_multiplier" in config and config["martingale_multiplier"] <= 0:
        errors.append("martingale_multiplier must be greater than 0.")

    if "take_profit" in config and config["take_profit"] <= 0:
        errors.append("take_profit must be greater than 0.")

    if "stop_loss" in config and config["stop_loss"] <= 0:
        errors.append("stop_loss must be greater than 0.")

    if "ticks" in config and config["ticks"] <= 0:
        errors.append("ticks must be greater than 0.")

    if errors:
        print("Configuration validation failed with the following errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("Configuration validation successful.")
    return True


def reset_to_default():
    """Reset the configuration to the default values."""
    save_default_config(DEFAULT_CONFIG)
    print("Configuration reset to default values.")


# Example usage
if __name__ == "__main__":
    # Load the default configuration
    config = load_default_config()

    # Display the loaded configuration
    print("Current configuration:")
    print(json.dumps(config, indent=4))

    # Validate the configuration
    if validate_config(config):
        print("Configuration is valid.")
    else:
        print("Configuration is invalid.")

    # Update specific fields in the configuration
    updates = {
        "take_profit": 50,
        "stop_loss": 50,
        "ticks": 2
    }
    config = update_default_config(config, updates)

    # Reset configuration to default
    reset_to_default()
