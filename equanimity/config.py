import os

from utils import load_yaml


config = load_yaml(os.path.expanduser('~/.equanimity/config.yml'))

COMPUTER_NAME = config['computer_name']

MEDIA_PATH = config['media_path']

DIRECTORIES = load_yaml(os.path.expanduser('~/.equanimity/directories.yml'))

DEVICES = load_yaml(os.path.expanduser('~/.equanimity/devices.yml'))

LOG_DIR = os.path.join(os.path.expanduser('~/.equanimity/logs'))

# Determine which backup device is present.
DEVICE = None
for d in DEVICES:
    if os.path.exists(d['path']):
        DEVICE = d
