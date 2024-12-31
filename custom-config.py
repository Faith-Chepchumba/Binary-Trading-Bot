import json
import os

# Paths to configuration files
CUSTOM_CONFIG_PATH = "config/custom-config.json"
DEFAULT_CONFIG_PATH = "config/default-config.json"

# Fallback to default configuration
DEFAULT_CONFIG = {
    "initial_stake": 0.35,
    "stake_list": [0.35, 0.43, 0.85, 1.74, 3.55, 7.3, 15, 31, 65, 130, 260],
    "martingale_multiplier": 2,
    "take_profit": 20,
    "stop_loss": 20,
    "ticks": 1
}


def load_default_config():
    """Load the default configuration as a fallback."""
    if os.path.exists(DEFAULT_CONFIG_PATH):
        with open(DEFAULT_CONFIG_PATH, "r") as file:
            return json.load(file)
    else:
        print("Default configuration file not found. Using hardcoded default values.")
        return DEFAULT_CONFIG


def load_custom_config():
    """Load the custom configuration, falling back to default if missing."""
    if not os.path.exists(CUSTOM_CONFIG_PATH):
        print(f"Custom configuration file not found. Creating a new one at {CUSTOM_CONFIG_PATH}.")
        save_custom_config(load_default_config())  # Create a custom config based on default
    with open(CUSTOM_CONFIG_PATH, "r") as file:
        config = json.load(file)
    print("Custom configuration loaded successfully.")
    return config


def save_custom_config(config):
    """Save the custom configuration file."""
    os.makedirs(os.path.dirname(CUSTOM_CONFIG_PATH), exist_ok=True)  # Ensure directory exists
    with open(CUSTOM_CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
    print(f"Custom configuration saved to {CUSTOM_CONFIG_PATH}.")


def update_custom_config(config, updates):
    """Update the custom configuration with new values."""
    for key, value in updates.items():
        if key in config:
            config[key] = value
            print(f"Updated '{key}' to {value}.")
        else:
            print(f"Key '{key}' not found in the configuration.")
    save_custom_config(config)
    return config


def validate_config(config):
    """Validate the custom configuration for required fields and correct values."""
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


def reset_to_custom():
    """Reset the custom configuration to the default values."""
    default_config = load_default_config()
    save_custom_config(default_config)
    print("Custom configuration reset to match the default configuration.")


def merge_with_default(custom_config):
    """Merge custom configuration with default, ensuring no missing fields."""
    default_config = load_default_config()
    merged_config = default_config.copy()
    merged_config.update(custom_config)
    print("Custom configuration merged with default values.")
    return merged_config


# Example usage
if __name__ == "__main__":
    # Load the custom configuration
    config = load_custom_config()

    # Display the loaded configuration
    print("Current custom configuration:")
    print(json.dumps(config, indent=4))

    # Validate the custom configuration
    if validate_config(config):
        print("Custom configuration is valid.")
    else:
        print("Custom configuration is invalid.")

    # Update specific fields in the custom configuration
    updates = {
        "take_profit": 50,
        "stop_loss": 50,
        "ticks": 2
    }
    config = update_custom_config(config, updates)

    # Merge the custom configuration with default values to fill missing fields
    merged_config = merge_with_default(config)
    print("Merged configuration:")
    print(json.dumps(merged_config, indent=4))

    # Reset custom configuration to default values
    reset_to_custom()
