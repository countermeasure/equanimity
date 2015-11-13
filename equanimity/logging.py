import os

from datetime import datetime

import config


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
