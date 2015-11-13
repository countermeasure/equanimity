import os

from utils import load_yaml

BASE_PATH = os.path.expanduser('~/.equanimity')

config = load_yaml(os.path.join(BASE_PATH, 'config.yml'))

COMPUTER_NAME = config['computer_name']

MEDIA_PATH = config['media_path']

DIRECTORIES = load_yaml(os.path.join(BASE_PATH, 'directories.yml'))

DEVICES = load_yaml(os.path.join(BASE_PATH, 'devices.yml'))

LOG_DIR = os.path.join(os.path.join(BASE_PATH, 'logs'))

# Determine which backup device is present.
DEVICE = None
for d in DEVICES:
    if os.path.exists(d['path']):
        DEVICE = d
