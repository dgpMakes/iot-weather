import yaml

def get_preferences(file):
    with open(file, 'rb') as f:
        conf = yaml.load(f.read())
    return conf