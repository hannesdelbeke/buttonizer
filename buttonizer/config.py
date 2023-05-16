"""
use load_config() to load a YAML or JSON
use save_config() to save to TAML or JSON, decided by the extension of the given path
"""
import json


def load_json(config_path) -> dict:
    """get json data from a file path, return None if not json"""
    path = str(config_path)
    if not path.lower().endswith(".json"):
        return

    with open(config_path) as file:
        data = json.load(file)
    return data


def load_yaml(config_path) -> dict:
    """get yaml data from a file path, return None if not yaml"""
    path = str(config_path)
    if not path.lower().endswith(".yaml"):
        return

    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def save_json(data, path):
    """save data to a json file"""
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def save_yaml(data, path):
    """save data to a yaml file"""
    with open(path, "w") as file:
        import yaml
        yaml.dump(data, file, default_flow_style=False)


def load_config(config_path) -> dict:
    """get data from a JSON or YAML config"""
    return load_json(config_path) or load_yaml(config_path)


def save_config(data, path):
    """save data to a JSON or YAML config"""
    if path.lower().endswith(".json"):
        save_json(data, path)
    elif path.lower().endswith(".yaml"):
        save_yaml(data, path)
    else:
        raise ValueError("Invalid config file extension")
