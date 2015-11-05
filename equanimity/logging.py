import os
import subprocess

from datetime import datetime

import config
from output import print_header
from utils import (
    checksum_directory,
    print_in_color,
)


def log(message):
    """
    Writes a line to the device's log.
    """
    device_log_path = os.path.join(
        config.LOG_DIR,
        '%s%s' % (config.DEVICE['name'], '.log')
    )
    with open(device_log_path, 'a') as f:
        f.write('%s\n' % message)


def write_log_headers():
    """
    Writes headers to log file.
    """
    log('- date: %s' % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    log('  source: %s' % config.COMPUTER_NAME)
    log('  directories:')


def sync_logs():
    """
    Copies all logs to the target device and verifies that the copy was
    successful.
    """
    print_header('Syncing logs to backup device')

    media_log_dir = os.path.join(
        config.MEDIA_PATH,
        config.DEVICE['name'],
        '.equanimity',
        'logs'
    )

    if not os.path.exists(media_log_dir):
        os.makedirs(media_log_dir)

    rsync_cmd = 'rsync -a --delete %s/ %s' % (config.LOG_DIR, media_log_dir)
    subprocess.call(rsync_cmd, shell=True)

    if checksum_directory(config.LOG_DIR) == checksum_directory(media_log_dir):
        print 'Logs synced successfully.'
    else:
        print_in_color('Logs NOT SYNCED.', 'red')
