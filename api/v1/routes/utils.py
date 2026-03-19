import os
import json
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File {file_path} not found")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON from file {file_path}")
        return None

def get_env_var(var_name, default=None):
    var_value = os.environ.get(var_name)
    if var_value is None:
        logging.warning(f"Environment variable {var_name} not set, using default value: {default}")
        return default
    return var_value

def make_get_request(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        return None