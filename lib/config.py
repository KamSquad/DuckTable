from json import load

config_path = 'config.json'


def get_argument(arg_name):
    params = {**load(open(config_path, "r"))}
    try:
        return params[arg_name]
    except KeyError:
        return None
